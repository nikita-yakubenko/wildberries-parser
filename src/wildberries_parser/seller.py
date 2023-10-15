import aiohttp

from .exceptions import NotFoundError


class Seller:
    """
    Class for work with Wildberries seller.
    """

    def __init__(self, seller_id: int, ordering: str='priceup') -> None:
        """
        Initial Seller object.

        seller_id - id of seller with we want to work.
        ordering - slug of needed ordering.
        """
        self.__seller_id = seller_id
        self.__ordering = ordering
        self.__create_urls()

    def __create_urls(self) -> None:
        """ Create map of needed urls. """
        self.__URLS_MAP: dict = {
            'products': f'https://catalog.wb.ru/sellers/catalog?appType=1&curr=rub&dest=-1257786&regions='
                         '80,38,83,4,64,33,68,70,30,40,86,75,69,1,31,66,22,110,48,71,114'
                        f'&sort={self.__ordering}&spp=0&supplier={self.__seller_id}',
            'info': f'https://suppliers-shipment.wildberries.ru/api/v1/suppliers/{self.__seller_id}',
        }

    async def get_products(self, page: int) -> dict:
        """ Get all seller products from current page. """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.__URLS_MAP["products"]}&page={page}') as resp:
                if resp.status == 200:
                    return await resp.json()
                raise NotFoundError('Продавец не найден. Проверьте введеный ID продавца!')

    async def get_info(self) -> dict:
        """ Get info about seller. """
        headers = {'x-client-name': 'site'}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__URLS_MAP['info'], headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise NotFoundError('Продавец не найден. Проверьте введеный ID продавца!')
