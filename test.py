def get_pagination(page: int):
    if page in range(1, 5):
        return [i for i in range(1, page + 2)]
    elif page > 4:
        return [1, "...", page - 1, page, page + 1]


print(get_pagination(20))
