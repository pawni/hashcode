from input_reader import InputReader
from output_writer import OutputWriter
import numpy
import math


class NaiveOptimiser:

    def __init__(self):
        input_reader = InputReader()
        self.state = input_reader.read(0)
        self.output_writer = OutputWriter('naive')
        self.num_rows = self.state['numRows']
        self.num_cols = self.state['numCols']
        self.num_drones = self.state['numDrones']
        self.num_turns = self.state['numTurns']
        self.max_payload = self.state['maxPayload']
        self.num_product_types = self.state['numProductTypes']
        self.product_weights = self.state['productWeights']
        self.num_warehouses = self.state['numWarehouses']
        # warehouse: liste auf dicts: x, y, items -> itemstock
        self.warehouse_data = self.state['warehousesData']
        # order data: liste auf dicts: x, y, numorders, items
        self.order_data = self.state['orderData']

        # get list of items
        self.item_lists = numpy.zeros((len(self.order_data), len(self.product_weights)), dtype=int)

        self.turns_used = numpy.zeros(self.num_drones)
        self.drone_location = numpy.zeros((self.num_drones, 2))

        for order_idx in numpy.arange(len(self.order_data)):
            for item in self.order_data[order_idx]['items']:
                self.item_lists[order_idx][item] += 1

        for n in numpy.arange(self.num_drones):
            self.drone_location[n] = [0, 0]

    def optimise(self):
        while True:
            print self.turns_used[:20]
            # Do smallest orders first
            # list of num orders
            num_orders = [order['numOrders'] for order in self.order_data]
            idx_smallest_orders = num_orders.index(min(num_orders))

            idx_order = idx_smallest_orders

            print self.item_lists[idx_smallest_orders]

            coordinates_smallest = (self.order_data[idx_order]['x'], self.order_data[idx_order]['y'])
            items_order = self.order_data[idx_order]['items']

            # get warehouses with items closest to destination that have at least one of the items stocked
            smallest_dist = 10000
            smallest_idx = -1

            # get warehouses that stock suitable items
            suitable_warehouses = []
            for warehouse in self.warehouse_data:
                warehouse_stock = warehouse['items']
                for item in items_order:
                    if warehouse_stock[item] > 0:
                        suitable_warehouses.append(warehouse)

            coordinates_warehouse = (0, 0)
            # get nearest one to customer
            for idx, warehouse in enumerate(suitable_warehouses):
                coordinates_warehouse = (warehouse['x'], warehouse['y'])
                dist = math.ceil(math.sqrt((coordinates_smallest[0] - coordinates_warehouse[0]) ** 2 + (
                    coordinates_smallest[1] - coordinates_warehouse[1]) ** 2))
                if dist < smallest_dist:
                    smallest_dist = dist
                    smallest_idx = idx

            cur_warehouse = self.warehouse_data[smallest_idx]

            # assign next drone which hasn't done much so for
            next_drone_idx = numpy.argmin(self.turns_used)

            # which stock?
            warehouse_stock = cur_warehouse['items']

            for idx, item in enumerate(self.item_lists[idx_order]):
                if item > 0:
                    print 'here'
                    if warehouse_stock[item] > 0:
                        # next drone fetch that stock!
                        # how many can it fetch?
                        num_possible = int(self.max_payload[next_drone_idx] * 1. / self.product_weights[item])

                        num_taken = min([num_possible, warehouse_stock[item]])

                        # calculate number of turns used
                        # add delivery
                        turn_count = smallest_dist + 1
                        load_dist = math.ceil(
                                numpy.linalg.norm(self.drone_location[next_drone_idx] - coordinates_warehouse))
                        turn_count += load_dist + 1

                        # we are over max turns!
                        if self.turns_used[next_drone_idx] + turn_count > self.num_turns:
                            self.end()
                            return
                        else:
                            self.turns_used[next_drone_idx] += turn_count

                        # fetch that
                        self.output_writer.writeLoad(next_drone_idx, smallest_idx, item, num_taken)
                        self.output_writer.writeDeliver(next_drone_idx, idx_order, item, num_taken)

                        # decrease warehouse stock
                        warehouse_stock[item] -= num_taken

                        # remove item from list
                        self.item_lists[idx_order][item] -= num_taken

                        # update drone location
                        self.drone_location[next_drone_idx] = coordinates_smallest
                        print 'here'
                        break
    def end(self):
        self.output_writer.endFile()


def main():
    no = NaiveOptimiser()
    no.optimise()
    # we are finished


if __name__ == "__main__":
    main()
