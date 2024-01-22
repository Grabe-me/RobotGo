import asyncio
import logging
import grpc  # type: ignore
from typing import AsyncIterable, Any
from robotgo.algorythm.algorythm import get_grid
from robotgo.services.robot_services.moving import Move
from robotgo.static.proto_files.test_pb2 import (
    Point,
    Field,
    MoveRequest,
    Motion,
    MoveResponse,
    Empty,
)
from robotgo.static.proto_files.test_pb2_grpc import (
    PathFinderServicer,
    add_PathFinderServicer_to_server,
)


class PathFinderService(PathFinderServicer):
    def __init__(self):
        self.field = None
        self.grid = None
        self.start = None
        self.targets = []
        self.current_point = None
        self.loop = None

    def reset(self):
        self.field = None
        self.grid = None
        self.start = None
        self.targets = []
        self.current_point = None

    async def SetField(self, request: Field, context: Any) -> Empty:
        self.reset()
        if self.check_data(request):
            logging.info("входные данные верны")
            asyncio.create_task(asyncio.to_thread(self.set_field, request, context))
        else:
            logging.warning("неверные входные данные")
        return Empty()

    @staticmethod
    def check_data(request: Field) -> bool:
        grid = "".join([letter for letter in request.grid if letter in ("0", "1")])
        return (
            request.N > 0
            and request.M > 0
            and len(request.grid) == (request.M * request.N) == len(grid)
        )

    def set_field(self, request: Field, context: Any) -> None:
        self.field = request
        self.grid = get_grid(self.field.N, self.field.M, self.field.grid)
        self.start = self.field.source

    def set_temp_props(self):
        if not self.current_point:
            self.current_point = self.start
        if self.current_point in self.targets:
            self.targets.remove(self.current_point)

    async def Moving(
        self, request_iterator: AsyncIterable[MoveRequest], context: Any
    ) -> AsyncIterable[MoveResponse]:
        if self.field is None:
            logging.warning("Field is not set.")
            async for _ in request_iterator:
                yield MoveResponse(direction=Motion.ERROR)
                return
        # ожидаем получения сетки
        while not self.grid:
            await asyncio.sleep(0.1)
        # проверка наличия цикла
        self.set_temp_props()
        async for move_request in request_iterator:
            # добавляем новые цели в список активных
            for target in move_request.targets:
                if not self.check_target(target):
                    yield MoveResponse(direction=Motion.ERROR)
                    return
                if target not in self.targets:
                    self.targets.append(target)
            # проходим по списку активных целей
            # расчитываем кратчайший путь для каждой цели
            move = Move(self.grid, self.current_point, self.targets)
            # вычисляем направление движения
            # записываем выбранное место как текущее
            direction, self.current_point = await move.next_step()
            logging.info(
                f"движение: {direction} "
                f"на позицию: "
                f"(x:{self.current_point.i}; y:{self.current_point.j})"
            )
            logging.warning("Невалидные данные для перемещения")
            # отправляем направление движения
            yield MoveResponse(direction=direction)

    def check_target(self, target: Point) -> bool:
        return (
            isinstance(target.i, int)
            and isinstance(target.j, int)
            and self.field.N > target.i >= 0
            and self.field.M > target.j >= 0
        )


async def serve() -> None:
    logging.info("starting server")
    server = grpc.aio.server()
    add_PathFinderServicer_to_server(PathFinderService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    logging.info("server listening on PORT 50051")
    await server.wait_for_termination()
