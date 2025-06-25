import mesa
import random
import matplotlib.pyplot as plt

class TraderAgent(mesa.Agent):

    def __init__(self, unique_id, model, agent_type, resources=10, budget=100):
        super().__init__(unique_id, model)
        self.type = agent_type  # "seller" ou "buyer"
        self.resources = resources if agent_type == "seller" else 0
        self.budget = budget if agent_type == "buyer" else 0
        self.price = random.uniform(5, 15) if agent_type == "seller" else None
        self.transactions = 0

    def step(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        neighbors = self.model.grid.get_cell_list_contents([self.pos])
        if self.type == "seller":
            self._interact_as_seller(neighbors)
        elif self.type == "buyer":
            self._interact_as_buyer(neighbors)

    def _interact_as_seller(self, neighbors):
        buyers = [a for a in neighbors if a.type == "buyer"]
        if buyers:
            buyer = self.random.choice(buyers)
            if buyer.budget >= self.price and self.resources > 0:
                buyer.budget -= self.price
                self.resources -= 1
                buyer.resources += 1
                self.transactions += 1
                buyer.transactions += 1
                self.price += 0.5  
        elif self.price > 1:
            self.price -= 0.5  

    def _interact_as_buyer(self, neighbors):
        sellers = [a for a in neighbors if a.type == "seller" and a.resources > 0]
        if sellers:
            seller = min(sellers, key=lambda x: x.price) 
            if seller.price <= self.budget:
                self.budget -= seller.price
                seller.resources -= 1
                self.resources += 1
                self.transactions += 1
                seller.transactions += 1
                seller.price += 0.5

class MarketModel(mesa.Model):

    def __init__(self, num_sellers, num_buyers, width=10, height=10):
        super().__init__()
        self.num_sellers = num_sellers
        self.num_buyers = num_buyers
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        self.schedule = mesa.time.RandomActivation(self)
        self.transactions_total = 0

        for i in range(self.num_sellers):
            seller = TraderAgent(i, self, "seller", resources=10)
            self._add_agent_randomly(seller)

        for i in range(self.num_buyers):
            buyer = TraderAgent(i + self.num_sellers, self, "buyer", budget=100)
            self._add_agent_randomly(buyer)

        self.datacollector = mesa.DataCollector(
            model_reporters={"Transactions": lambda m: m.transactions_total},
            agent_reporters={"Price": lambda a: a.price if a.type == "seller" else None}
        )

    def _add_agent_randomly(self, agent):
        self.schedule.add(agent)
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))

    def step(self):
        self.transactions_total = sum(agent.transactions for agent in self.schedule.agents)
        self.datacollector.collect(self)
        self.schedule.step()

def plot_transactions(model):

    data = model.datacollector.get_model_vars_dataframe()
    plt.figure(figsize=(8, 4))
    plt.plot(data["Transactions"])
    plt.xlabel("Steps")
    plt.ylabel("Total Transactions")
    plt.title("Market Transactions Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_average_price(model):

    agent_data = model.datacollector.get_agent_vars_dataframe()
    seller_prices = agent_data[agent_data["Price"].notnull()]["Price"]
    plt.figure(figsize=(8, 4))
    plt.plot(seller_prices.groupby(level=0).mean())
    plt.xlabel("Steps")
    plt.ylabel("Average Seller Price")
    plt.title("Average Seller Price Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    model = MarketModel(num_sellers=10, num_buyers=20)
    for _ in range(100): 
        model.step()

    plot_transactions(model)
    plot_average_price(model)
