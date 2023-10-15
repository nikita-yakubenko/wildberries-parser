import asyncio

from .seller import Seller
from .product import Product


class WildberriesParser:
    """
    Facade for all WB parsing features.
    """

    seller_class = Seller
    product_class = Product

    # WB bussines logic provide access max to 10000 seller items
    SELLER_MAX_PRODUCTS = 9999

    def __init__(self, concurents: int=200) -> None:
        self.__semaphore = asyncio.Semaphore(concurents)

    def get_products_by_seller(self, seller_id: int, max_products: int, ordering: str) -> list:
        """
        Get list of product of seller.
        seller_id - id of seller on WB;
        max_products - max count to parse;
        ordering - apply sorting;
        """
        if max_products > self.SELLER_MAX_PRODUCTS:
            raise ValueError(f'Value of parameter max_products must be lower than {self.SELLER_MAX_PRODUCTS+1}')
        max_pages = max_products // 100 + 1
        results = asyncio.run(
            self.get_products_by_seller_async(seller_id=seller_id, max_pages=max_pages, ordering=ordering))
        products = []
        for result in results:
            products.extend(result['data']['products'])
        return products[:max_products]

    async def get_products_by_seller_async(self, seller_id: int, max_pages: int, ordering: str) -> list:
        """ Create async tasks for get seller products and run it. """
        tasks = []
        for page in range(1, max_pages+1):
            task = asyncio.ensure_future(self.products_by_seller(seller_id=seller_id, page=page, ordering=ordering))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

    async def products_by_seller(self, seller_id: int, page: int, ordering: str):
        """ Get seller products on current page with selected sorting. """
        seller = self.seller_class(seller_id=seller_id, ordering=ordering)
        prs = asyncio.create_task(seller.get_products(page=page))
        await prs
        return prs.result()

    def get_products_data(self, product_ids: list):
        """ Get products data. """
        results = asyncio.run(self.get_products_data_async(product_ids))
        return results

    async def get_products_data_async(self, product_ids: list):
        """ Create async tasks for get products data and run it. """
        tasks = []
        for product_id in product_ids:
            task = asyncio.ensure_future(self.get_full_product_data(product_id))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

    async def get_full_product_data(self, product_id):
        """ Get full product data. """
        pr = self.product_class(product_id=product_id)
        main = asyncio.create_task(pr.get_main())
        detail = asyncio.create_task(pr.get_detail())
        prices = asyncio.create_task(pr.get_price_history())
        sold_count = asyncio.create_task(pr.get_sold_count())
        seller = asyncio.create_task(pr.get_seller())
        image = asyncio.create_task(pr.get_image_link())
        async with self.__semaphore:
            await main
            await detail
            await prices
            await sold_count
            await seller
            await image
        product_data_dict = {
            'main':main.result(),
            'detail': detail.result(),
            'prices': prices.result(),
            'sold_count': sold_count.result(),
            'seller': seller.result(),
            'image': image.result()}
        return product_data_dict

    def get_seller_info(self, seller_id: int):
        """ Get info about seller. """
        results = asyncio.run(self.get_seller_info_async(seller_id))
        return results.result()

    async def get_seller_info_async(self, seller_id):
        seller = self.seller_class(seller_id=seller_id)
        info = asyncio.create_task(seller.get_info())
        await info
        return info
