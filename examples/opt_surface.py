__author__ = 'indiquant'


from finalytics.utils.dbhelper import EnumDBOptionTable, read_rectimes, read_options
from finalytics.product.option import PutCallSurface


def main():
    rectimes = read_rectimes('NIFTY', 20160921)
    for rectime in rectimes:
        optrows = read_options('NIFTY', 20160921, rectime)
        surf = consume_surface('NIFTY', optrows)
        c_grid, _ = surf.get_grid('C')
        p_grid, _ = surf.get_grid('P')
        print('pause')
        # TODO: add your code here

    print('stop')


def consume_surface(undl, optrows):
    surf = PutCallSurface(undl)



    for optrow in optrows:
        surf.add(
            optrow[EnumDBOptionTable.opt_type.value - 1],
            optrow[EnumDBOptionTable.expiry.value - 1],
            optrow[EnumDBOptionTable.strike.value - 1],
            optrow[EnumDBOptionTable.bidpx.value - 1],
            optrow[EnumDBOptionTable.askpx.value - 1],
            optrow[EnumDBOptionTable.lastpx.value - 1],
            optrow[EnumDBOptionTable.volume.value - 1])

    return surf


if __name__ == '__main__':
    main()