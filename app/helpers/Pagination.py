from math import ceil

class Pagination:
    def __init__(self, total, current_page, per_page):
        self.total = total
        self.per_page = per_page
        self.current_page = current_page

    @property
    def last_pages(self):
        return int(ceil(float(self.total) / float(self.per_page)))

    @property
    def prev_page(self):
        if self.current_page == 1:
            return None
        else:
            return self.current_page - 1

    @property
    def next_page(self):
        if self.current_page == self.last_pages:
            return None
        else:
            return self.current_page + 1

    @property
    def start(self):
        return self.current_page * self.per_page - self.per_page + 1

    @property
    def end(self):
        return self.current_page * self.per_page

    @property
    def display(self):
        pages = []
        # if self.last_pages <= 10:
        #     for i in range(self.last_pages):
        #         pages.append(i + 1)
        # elif self.current_page <= 6:
        #     for i in range(10):
        #         pages.append(i + 1)
        # else:
        #     start = self.current_page - 5
        #     end = self.current_page + 4
        #
        #     if end > self.last_pages:
        #         end = self.last_pages
        #         start = end - 10
        #
        #     for i in range(start, end + 1, 1):
        #         pages.append(i)

        if self.last_pages <= 8:
            for i in range(self.last_pages):
                pages.append(i + 1)
        elif self.current_page <= 3:
            pages = [1,2,3,4,5, -1, self.last_pages]
        elif self.current_page <= 5:
            pages = []
            for i in range(1, self.current_page + 3, 1):
                pages.append(i)
            pages.append(-1)
            pages.append(self.last_pages)
        elif self.current_page >= self.last_pages - 3:
            pages = [1, -1]
            for i in range(self.last_pages - 5, self.last_pages + 1, 1):
                pages.append(i)
        elif self.current_page >= self.last_pages - 5:
            pages = [1, -1]
            for i in range(self.current_page - 2, self.last_pages + 1, 1):
                pages.append(i)
        else:
            pages = [1, -1]
            for i in range(self.current_page - 2, self.current_page + 3, 1):
                pages.append(i)
            pages.append(-1)
            pages.append(self.last_pages)

        return pages
