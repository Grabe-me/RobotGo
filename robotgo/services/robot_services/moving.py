import asyncio
from concurrent.futures import ProcessPoolExecutor
from robotgo.algorythm import algorythm, Node
from robotgo.static.proto_files.test_pb2 import Point, Motion


class Move:

    def __init__(self, grid: list[list[Node]], current_point: Point, targets: list[Point]):
        self.grid = grid
        self.targets = targets
        self.current_point = current_point
        self.loop = asyncio.get_event_loop()

    @property
    def current_point(self):
        return self._current_point

    @current_point.setter
    def current_point(self, value):
        if isinstance(value, Node):
            self._current_point = self.node_to_point(value)
        elif isinstance(value, Point):
            self._current_point = value

    @staticmethod
    def point_to_node(point):
        return Node(x=point.i, y=point.j)

    @staticmethod
    def node_to_point(node):
        return Point(i=node.x, j=node.y)

    async def finding_out_best_way(self) -> list[Node]:
        best_way: list[Node] = []
        with ProcessPoolExecutor() as executor:
            tasks = [self.loop.run_in_executor(executor, algorythm, (self._current_point.i, self._current_point.j),
                                               (target.i, target.j), self.grid) for target in self.targets]
            results = await asyncio.gather(*tasks)

            for target, result in zip(self.targets, results):
                if len(result) > 1 and (not best_way or len(best_way) > len(result)):
                    best_way = result

        return best_way

    async def next_step(self):
        way = await self.finding_out_best_way()
        motion = None
        if not way:
            motion = Motion.FINISH
            next_step = self._current_point
        else:
            next_step = self.node_to_point(way[1])
            if self._current_point.i - next_step.i > 0:
                motion = Motion.UP
            elif self._current_point.i - next_step.i < 0:
                motion = Motion.DOWN
            else:
                if self._current_point.j - next_step.j < 0:
                    motion = Motion.RIGHT
                elif self._current_point.j - next_step.j > 0:
                    motion = Motion.LEFT

        return motion, next_step
