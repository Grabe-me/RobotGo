import asyncio
import logging
import grpc  # type: ignore
from robotgo.static.proto_files.test_pb2 import MoveRequest, Field, Point
from robotgo.static.proto_files.test_pb2_grpc import PathFinderStub


async def set_field(stub, field):
    # Отправить унарный запрос SetField
    empty_response = await stub.SetField(field)
    print("SetField response:", empty_response)


async def move_robot(stub, targets):
    # Создать потоковый запрос MoveRequest
    move_request = MoveRequest(targets=targets)

    # Отправить двусторонний потоковый запрос Moving
    response_iterator = stub.Moving(iter([move_request]))

    async for response in response_iterator:
        print("MoveResponse received:", response)


async def main():
    # Установка соединения с сервером
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        # Создание клиентского stub
        stub = PathFinderStub(channel)
        # Пример использования унарного запроса SetField
        field = Field(N=5, M=4, source=Point(i=0, j=0), grid="01010010100001000000")
        await set_field(stub, field)
        """
        0 1 0 1
        0 0 1 0
        1 0 0 0
        0 1 0 0
        0 0 0 0
        """

        # Пример использования двустороннего потокового запроса MoveRequest
        targets = [Point(i=3, j=0), Point(i=2, j=3), Point(i=4, j=3)]
        await move_robot(stub, targets)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
