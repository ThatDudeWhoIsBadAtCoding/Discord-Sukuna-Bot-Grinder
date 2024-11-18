import requests
from bs4 import BeautifulSoup


class Card_Tree():
    def __init__(self, id, master_ace):

        self.id = id
        self.ace = master_ace
        self.tree = ""
        self.name = ""
        
    def get_ace(self, cards, level):
        for card in cards[:-1]:
            text = card.get("alt")
            if "Ace" in text and text[-1] == level:
                tree = card.parent.next_sibling
                links = []
                names = []
                levels = []
                for c in tree.children:
                    n = c.find("a")
                    name = n.next_sibling.get_text()
                    ace_required = n.next_sibling.next_sibling.get_text()
                    id = n.get("href")
                    links.append(f"https://sukunabot.xyz/ace/{id}")
                    names.append(name)
                    levels.append(ace_required[-1])
        try:
            links = links if len(links) else None
            return links, names, levels
        except:
            return None, None, None


    def card_rabbithole(self, cards, names, levels, depth, for_logger=False):
        if cards is None: return self.tree
        for card, name, level in zip(cards, names, levels):

            resp = requests.get(card)

            soup = BeautifulSoup(resp.content, "html.parser")
                
            links_ = soup.find_all("img")

            s = "\u2014" * depth if not for_logger else "-"

            self.tree += f"\n{s}{name} A{level}"

            c, n, l = self.get_ace(links_, level)
            self.card_rabbithole(c, n, l, depth + 1, for_logger)
    
    def set_name(self):
        url = f"https://sukunabot.xyz/ace/{self.id}"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser") 
        links_ = soup.find_all("img")
        self.name = links_[-1].next_sibling.get_text().split(" (")[0] 


    def get_card_tree(self, for_logger=False):


        url = f"https://sukunabot.xyz/ace/{self.id}"

        resp = requests.get(url)

        soup = BeautifulSoup(resp.content, "html.parser")

            
        links_ = soup.find_all("img")

        self.name = links_[-1].next_sibling.get_text().split(" (")[0] 
        

        self.tree = f"{self.name} Ace {self.ace} requires:-" if not for_logger else f"{self.id}-{self.name}-{self.ace}"

        c, n, l = self.get_ace(links_, self.ace)

        self.card_rabbithole(c, n, l, 1, for_logger)

        return self.tree
    
    def track_ace(self):
        self.set_name()
        with open("ace_tracker.txt", "r") as file:
            content = file.read()
            if f"-{self.name} A{self.ace}" in content or f"{self.id}-{self.name}-{self.ace}" in content:
                return -1
        tree = self.get_card_tree(for_logger=True)
        with open("ace_tracker.txt", "a") as file:
            file.write(tree + "\n")
    
    def untrack_ace(self):
        new_lines = []
        self.set_name()
        flag_found = False
        with open("ace_tracker.txt", "r") as f:
            for line in f.readlines():
                if line.startswith(self.id):
                    flag_found = True
                    continue
                if line.startswith("-") and flag_found:
                    continue
                elif flag_found:
                    flag_found = False
                new_lines.append(line)
        
        with open("ace_tracker.txt", "w") as f:
            f.writelines(new_lines)