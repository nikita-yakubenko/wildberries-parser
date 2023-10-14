import asyncio
import aiohttp
import math

from .exceptions import NotFoundError


class Product:
	"""
	Class for work with WB product.
	Create this class for every product you need to work.
	"""

	def __init__(self, product_id: int) -> None:
		"""
		Initial Product object.
		product_id - id of product with we want to work.
		"""
		self.__product_id = product_id
		self.__vol = self.__get_vol()
		self.__part = self.__get_part()
		self.__vhost = self.__get_vhost()
		self.__create_urls()
		self.__session = aiohttp.ClientSession()

	def __del__(self) -> None:
		""" Async delete created aiohttp session on object destroy. """
		asyncio.run(self._close_session())

	async def _close_session(self) -> None:
		""" Close aiohttp session. """
		if not self.__session.closed:
			await self.__session.close()

	def __create_urls(self) -> None:
		""" Create map of needed urls. """
		self.__URLS_MAP: dict = {
			'main': f'https://{self.__vhost}/vol{self.__vol}/part{self.__part}/{self.__product_id}/info/ru/card.json',
			'detail': f'https://card.wb.ru/cards/detail?appType=1&curr=rub&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,1,31,66,22,110,48,71,114&spp=0&nm={self.__product_id}',
			'price_history': f'https://{self.__vhost}/vol{self.__vol}/part{self.__part}/{self.__product_id}/info/price-history.json',
			'sold_count': f'https://product-order-qnt.wildberries.ru/v2/by-nm/?nm={self.__product_id}',
			'seller': f'https://{self.__vhost}/vol{self.__vol}/part{self.__part}/{self.__product_id}/info/sellers.json',
			'image': f'https://{self.__vhost}/vol{self.__vol}/part{self.__part}/{self.__product_id}/images/big/1.webp',
		}

	def __get_vol(self) -> int:
		""" Calculate the volume number in which the current product is stored. """
		return math.floor(self.__product_id/100000)

	def __get_part(self) -> int:
		""" Calculate the part number in which the current product is stored. """
		return math.floor(self.__product_id/1000)

	def __get_vhost(self) -> str:
		""" Calculate the virtual host in which the current product is stored. """
		match self.__vol:
			case num if 0 <= num <=  143:
			    t = "01"
			case num if 144 <= num <= 287:
			    t = "02"
			case num if 288 <= num <= 431:
			    t = "03"
			case num if 432 <= num <= 719:
			    t = "04"
			case num if 720 <= num <= 1007:
			    t = "05"
			case num if 1008 <= num <= 1061:
			    t = "06"
			case num if 1062 <= num <= 1115:
			    t = "07"
			case num if 1116 <= num <= 1169:
			    t = "08"
			case num if 1170 <= num <= 1313:
			    t = "09"
			case num if 1314 <= num <= 1601:
			    t = "10"
			case num if 1602 <= num <= 1655:
			    t = "11"
			case num if 1656 <= num <= 1919:
			    t = "12"
			case num if 1920 <= num <= 2045:
			    t = "13"
			case _:
			    t = "14"
		return f'basket-{t}.wb.ru'

	async def get_main(self) -> dict:
		""" Get main data of current product. """
		async with self.__session.get(self.__URLS_MAP['main']) as resp:
			if resp.status == 200:
				return await resp.json()
			raise NotFoundError(f'Cant find main data for product with id={self.__product_id}')
	
	async def get_detail(self) -> dict:
		""" Get detail data of current product. """
		async with self.__session.get(self.__URLS_MAP['detail']) as resp:
			if resp.status == 200:
				return await resp.json()
			raise NotFoundError(f'Cant find detail data for product with id={self.__product_id}')
	
	async def get_price_history(self) -> dict:
		""" Get price history of current product. """
		async with self.__session.get(self.__URLS_MAP['price_history']) as resp:
			if resp.status==200:
				return await resp.json()
			else:
				return {}
	
	async def get_sold_count(self) -> dict:
		""" Get detail sold count of current product. """
		async with self.__session.get(self.__URLS_MAP['sold_count']) as resp:
			if resp.status == 200:
				return await resp.json()
			raise NotFoundError(f'Cant find sold count data for product with id={self.__product_id}')
	
	async def get_seller(self) -> dict:
		""" Get seller of current product. """
		async with self.__session.get(self.__URLS_MAP['seller']) as resp:
			if resp.status == 200:
				return await resp.json()
			raise NotFoundError(f'Cant find seller for product with id={self.__product_id}')

	async def get_image_link(self) -> dict:
		""" Get big image of current product. """
		return self.__URLS_MAP['image']
