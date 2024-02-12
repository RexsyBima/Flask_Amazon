from app.models import SQLProducts, PYProducts


def Item(sql_query: SQLProducts):
    return PYProducts(
        id=sql_query.id,
        url=sql_query.url,
        title=sql_query.title,
        price=sql_query.price,
        total_rating=sql_query.total_rating,
        rating=sql_query.rating,
        brand=sql_query.brand,
        img_url=sql_query.img_url,
    )


def Items(sql_query: SQLProducts):
    return [
        PYProducts(
            id=item.id,
            url=item.url,
            title=item.title,
            price=item.price,
            total_rating=item.total_rating,
            rating=item.rating,
            brand=item.brand,
            img_url=item.img_url,
        )
        for item in sql_query
    ]


def rating_star(rating_val: float):
    rating_val = int(rating_val)
    return [1 if i < rating_val else 0 for i in range(0, 5)]
