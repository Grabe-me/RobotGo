import asyncio
import logging
import grpc
from typing import AsyncIterable
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

    async def SetField(self, request: Field, context) -> Empty:
        self.reset()
        asyncio.create_task(asyncio.to_thread(self.set_field, request, context))
        return Empty()

    def set_field(self, request: Field, context) -> None:
        self.field = request
        self.grid = get_grid(self.field.N, self.field.M, self.field.grid)
        self.start = self.field.source

    def set_temp_props(self):
        if not self.current_point:
            self.current_point = self.start
        if self.current_point in self.targets:
            self.targets.remove(self.current_point)

    async def Moving(
        self, request_iterator: AsyncIterable[MoveRequest], context
    ) -> AsyncIterable[MoveResponse]:
        if self.field is None:
            print("Error: Field is not set.")
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
                if target not in self.targets:
                    self.targets.append(target)
            # проходим по списку активных целей
            # расчитываем кратчайший путь для каждой цели

            move = Move(self.grid, self.current_point, self.targets)
            # вычисляем направление движения
            # записываем выбранное место как текущее
            next_step, self.current_point = await move.next_step()
            logging.info(
                f"current position: "
                f"(x:{self.current_point.i}; y:{self.current_point.j}) "
                f"direction: {next_step}"
            )
            # отправляем направление движения
            yield MoveResponse(direction=next_step)


async def serve() -> None:
    logging.info("starting server")
    server = grpc.aio.server()
    add_PathFinderServicer_to_server(PathFinderService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    logging.info("server listening on PORT 50051")
    await server.wait_for_termination()
