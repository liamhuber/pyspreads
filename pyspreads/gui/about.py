import ipywidgets as widgets


class About:
    def __init__(self):
        content = """
        Some placeholder until I have the readme written and can steal from there.
            
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et 
        dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex 
        ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu 
        fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt 
        mollit anim id est laborum.
        """
        self.screen = widgets.HTML(
            value='<style>p{word-wrap: break-word}</style> <p>' + content + ' </p>'
        )
