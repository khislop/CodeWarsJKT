import random as rand
import api.units as lib
from api.units import SpecialPowers

NAME = "JKT"
SCHOOL = "Colorado School of Mines"



def CheckTile(tile, map):
    # print map.height
    # print map.width
    # print tile.x
    # print tile.y
    # print map.tiles[0][0]
    
    left = right = down = up = None
    if tile.x - 1 >= 0:
        left = map.tiles[tile.x - 1][tile.y].hotel
    if tile.y - 1 >= 0:
        down = map.tiles[tile.x][tile.y - 1].hotel
    if tile.x + 1 < map.width:
        right = map.tiles[tile.x + 1][tile.y].hotel
    if tile.y + 1 < map.height:
        up = map.tiles[tile.x][tile.y + 1].hotel
    return [left,right,down,up]

def MergeOwn(tiles, map, name):
    #print "OUR GUID =====================   "
    #print name
    for tile in tiles:
        tile_hotels = CheckTile(tile, map)
        unique_hotels = []
        count = 0
        for hotel in tile_hotels:
            if hotel != None:
                if hotel not in unique_hotels:
                    unique_hotels.append(hotel)
        for hotel in unique_hotels:
            #print "OWNER BELOW---------------------------------"
            #print hotel.name
            for owner in hotel.owners:
                if name is owner.num_shares:
                    count =  count + 1
        if count >= 2:
            return tile

    return None

def MergeBigger(tiles, map, name):
    for tile in tiles:
        tile_hotels = CheckTile(tile, map)
        unique_hotels = []
        for hotel in tile_hotels:
            if hotel != None:
                if hotel not in unique_hotels:
                    unique_hotels.append(hotel)
        for hotel in unique_hotels:
            for owner in hotel.owners:
                if name is owner.num_shares:
        

    return None

def random_element(list):
    if len(list) < 1:
        print "random element from empty list? returning None..."
        return None
    return list[rand.randint(0, len(list) - 1)]

def SelectTile(tiles, map, name):
    tile = MergeOwn(tiles, map, name)
    if tile != None:
        return tile
    tile = MergeBigger(tiles, map, name)
    return random_element(tiles)







class MyPlayerBrain(object):
    """The Python AI class."""

    def __init__(self):
        self.name = NAME
        self.school = SCHOOL
        if NAME is "Anders Hejlsberg" or SCHOOL is "Windward U.":
            print "Please enter your name and university at the top of MyPlayerBrain.py"

            #The player's avatar (looks in the same directory that this module is in).
            #Must be a 32 x 32 PNG file.
        try:
            avatar = open("MyAvatar.png", "rb")
            avatar_str = b''
            for line in avatar:
                avatar_str += line
            avatar = avatar_str
        except IOError:
            avatar = None # avatar is optional
        self.avatar = avatar

    def Setup(self, map, me, hotelChains, players):
        print "in setup----------------------------------"
        pass #any setup code...

    def QuerySpecialPowersBeforeTurn(self, map, me, hotelChains, players):
        print "in QuerySpecialPowersBeforeTurn -----------------------------"
        if rand.randint(0, 29) == 1:
            return SpecialPowers.DRAW_5_TILES
        if rand.randint(0, 29) == 1:
            return SpecialPowers.PLACE_4_TILES
        return SpecialPowers.NONE

    def QueryTileOnly(self, map, me, hotelChains, players):
        print "in QueryTileOnly--------------------------------"
        tile = random_element(me.tiles)
        createdHotel = next((hotel for hotel in hotelChains if not hotel.is_active), None)
        mergeSurvivor = next((hotel for hotel in hotelChains if hotel.is_active), None)
        return PlayerPlayTile(tile, createdHotel, mergeSurvivor)


    def QueryTileAndPurchase(self, map, me, hotelChains, players):
        print "in QueryTileAndPurchase--------------------------------"
        #print map
        inactive = next((hotel for hotel in hotelChains if not hotel.is_active), None)
        turn = PlayerTurn(tile=SelectTile(me.tiles, map, me.guid), created_hotel=inactive, merge_survivor=inactive)
        turn.Buy.append(lib.HotelStock(random_element(hotelChains), rand.randint(1, 3)))
        turn.Buy.append(lib.HotelStock(random_element(hotelChains), rand.randint(1, 3)))

        if rand.randint(0, 20) is not 1:
            return turn
        temp_rand = rand.randint(0, 2)
        if temp_rand is 0:
            turn.Card = SpecialPowers.BUY_5_STOCK
            turn.Buy.append(lib.HotelStock(random_element(hotelChains), 3))
            return turn
        elif temp_rand is 1:
            turn.Card = SpecialPowers.FREE_3_STOCK
            return turn
        else:
            if (len(me.stock) > 0):
                turn.Card = SpecialPowers.TRADE_2_STOCK
                turn.Trade.append(TradeStock(random_element(me.stock).chain, random_element(hotelChains)))
                return turn

    def QueryMergeStock(self, map, me, hotelChains, players, survivor, defunct):
        print "in QueryMergeStock----------------------------------------"
        myStock = next((stock for stock in me.stock if stock.chain == defunct.name), None)
        return PlayerMerge(myStock.num_shares / 3, myStock.num_shares / 3, (myStock.num_shares + 2) / 3)




class PlayerMerge(object):
    def __init__(self, sell, keep, trade):
        self.Sell = sell
        self.Keep = keep
        self.Trade = trade


class PlayerPlayTile(object):
    def __init__(self, tile, created_hotel, merge_survivor):
        self.Tile = tile
        self.CreatedHotel = created_hotel
        self.MergeSurvivor = merge_survivor


class PlayerTurn(PlayerPlayTile):
    def __init__(self, tile, created_hotel, merge_survivor):
        super(PlayerTurn, self).__init__(tile, created_hotel, merge_survivor)
        self.Card = lib.SpecialPowers.NONE
        self.Buy = []   # hotel stock list
        self.Trade = []    # trade stock list


class TradeStock(object):
    def __init__(self, trade_in, get):
        self.Trade = trade_in
        self.Get = get
