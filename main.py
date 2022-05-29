from enum import Enum, auto
import matplotlib.pyplot as plt
import random


class Algorithm:
    def __init__(self, number_of_cells_per_side: int,
                 product_storage: int,
                 number_of_iterations: int,
                 percentage_of_consumers: int,
                 percentage_of_advertising: int) -> None:

        self.__number_of_cells_per_side = number_of_cells_per_side
        self.__percentage_of_consumers = percentage_of_consumers
        self.__product_storage = product_storage
        self.__number_of_iterations = number_of_iterations
        self.__percentage_of_advertising = percentage_of_advertising

        # Initialize population
        self.__population = [[User() for x in range(number_of_cells_per_side)]
                             for y in range(number_of_cells_per_side)]

        self.__clients, self.__potential_clients = 0, number_of_cells_per_side ** 2


    def run(self) -> None:
        for day in range(self.__number_of_iterations):
            self.one_day()

    def number_users_and_day(self):
        for day in range(self.__number_of_iterations):
            yield self.__clients, self.__potential_clients, day
            self.one_day()

    def one_day(self) -> None:
        for y in range(self.__number_of_cells_per_side):
            for x in range(self.__number_of_cells_per_side):
                selected_user = self.__population[x][y]
                self.user_check(selected_user, position=(x, y))

    def user_check(self, selected_user, position):
        if selected_user.state == UserStates.default and is_user_buy_product(self.__percentage_of_consumers):
            selected_user.change_state_to_bought(self.__product_storage)
            self.change_number_of_clients_and_potential_clients(add_client=True)
            x, y = position
            users = self.__get_default_users_nearby(x, y)
            neighbor = advertise_product_to_neighbor(users, self.__percentage_of_advertising)
            if neighbor is not None:
                self.change_number_of_clients_and_potential_clients(add_client=True)
                neighbor.change_state_to_bought(self.__product_storage)
        elif selected_user.state == UserStates.bought:
            selected_user.end_day()
            if selected_user.product_storage <= 0:
                selected_user.change_state_to_default()
                self.change_number_of_clients_and_potential_clients()
        # print(f"Buyers: {self.__clients}; potential buyers: {self.__potential_clients}")

    def __get_default_users_nearby(self, x: int, y: int):
        max_cells = self.__number_of_cells_per_side

        up = self.__population[x][y + 1] if y + 1 < max_cells else None
        down = self.__population[x][y - 1] if y - 1 >= 0 else None

        right_up = self.__population[x + 1][y + 1] if x + 1 < max_cells and y + 1 < max_cells else None
        right = self.__population[x + 1][y] if x + 1 < max_cells else None
        right_down = self.__population[x + 1][y - 1] if x + 1 < max_cells and y - 1 >= 0 else None

        left_up = self.__population[x - 1][y + 1] if x - 1 >= 0 and y + 1 < max_cells else None
        left = self.__population[x - 1][y] if x - 1 >= 0 else None
        left_down = self.__population[x - 1][y - 1] if x - 1 >= 0 and y - 1 >= 0 else None

        searched_users = (up, down, right_up, right, right_down, left_up, left, left_down)
        return get_only_default_users(searched_users)

    def change_number_of_clients_and_potential_clients(self, add_client=False):
        if add_client:
            self.__clients += 1
            self.__potential_clients -= 1
        else:
            self.__clients -= 1
            self.__potential_clients += 1

class User:
    def __init__(self):
        self.__state = UserStates.default
        self.__product_storage = 0

    @property
    def state(self):
        return self.__state

    @property
    def product_storage(self):
        return self.__product_storage

    def change_state_to_bought(self, product_storage: int):
        self.__state = UserStates.bought
        self.__product_storage = product_storage

    def change_state_to_default(self):
        self.__state = UserStates.default
        self.__product_storage = 0

    def end_day(self):
        if self.__state == UserStates.bought:
            self.__product_storage -= 1
        else:
            raise Exception("The user does not have a product")



class UserStates(Enum):
    default = auto()
    bought = auto()

def __clear_from_none_and_find_default_users(user):
    if user is None:
        return None
    else:
        return user if user.state == UserStates.default else None


def get_only_default_users(users):
    return tuple(filter(__clear_from_none_and_find_default_users, users))


def is_user_buy_product(percentage_of_consumers):
    value = random.randint(0, 100)
    return value <= percentage_of_consumers


def advertise_product_to_neighbor(neighbors, percentage_of_advertising):
    for neighbor in neighbors:
        if is_user_buy_product(percentage_of_advertising):
            return neighbor
    return None

def main(**kwargs) -> None:
    number_of_cells_per_side = kwargs["number_of_cells_per_side"]
    product_storage = kwargs["product_storage"]
    number_of_iterations = kwargs["number_of_iterations"]
    percentage_of_consumers = kwargs["percentage_of_consumers"]
    percentage_of_advertising = kwargs["percentage_of_advertising"]

    algorithm = Algorithm(number_of_cells_per_side=number_of_cells_per_side,
                          product_storage=product_storage,
                          number_of_iterations=number_of_iterations,
                          percentage_of_consumers=percentage_of_consumers,
                          percentage_of_advertising=percentage_of_advertising)
    buyers = []
    potential_buyers = []
    days = []

    fig, ax = plt.subplots()

    for buyers_y, potential_buyers_y, day_x in algorithm.number_users_and_day():
        buyers.append(buyers_y)
        potential_buyers.append(potential_buyers_y)
        days.append(day_x)

    ax.stackplot(days, potential_buyers, buyers, alpha=0.8, labels=['Потенциальный клиент', 'Клиент'])

    ax.set_title("Популяция агентов")
    ax.legend(loc='lower right')
    ax.set_xlabel("Дни")
    ax.set_ylabel("Пользователи")

    ax.set_xlim(xmin=days[0], xmax=days[-1])
    fig.tight_layout()

    plt.show()


if __name__ == '__main__':
    main(number_of_cells_per_side=150,
         product_storage=25,
         number_of_iterations=35,
         percentage_of_consumers=15,
         percentage_of_advertising=2)