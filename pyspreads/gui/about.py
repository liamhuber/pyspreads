import ipywidgets as widgets


# Styling https://github.com/jupyter-widgets/ipywidgets/issues/1333
class About:
    def __init__(self):
        content = """
        Welcome to pyspreads, a small app for playing around with vertical spreads in options trading.
        </br>
        </br>
        On the trade screen you can click on options contracts to add or remove them from your overall position. Plots 
        of the value of this position (at expiry) relative to movement of the underlying asset are then automatically 
        updated. Click the contract again to remove it from your position. This screen also gives you a visual summary 
        of the market, showing the premiums for contracts as a function of strike price, as well as deviations from a 
        smoothed value of these premiums. You can see the positons and market plots in higher resolution on their 
        respective tabs. 
        </br>
        </br>
        Across all of these you will see and "expectation" curve, showing a metric for the expected price of the 
        underlying asset. This is based on the available options contracts. In particular, it is a normalized 
        probability based on the inverse exponential of one over the out-of-the-money ask price for the options 
        contract. It is great for getting a quick sense of what the options prices tell you about overall market 
        sentiment and expected momentum of the asset, but take it with a huge grain of salt -- it is literally just the 
        first model that popped into my head, and does not yet reflect any research into real models of options pricing 
        and asset price expectations.
        </br>
        </br>
        The app comes pre-loaded with some SPY options from October 2022 that expire in December 2022, but in the 
        Load data tab you can copy and paste in columnar data of your own for analysis.
        </br>
        </br>
        This app is copyright 2022 Liam Huber, released under the BSD3 license. 
        You can read more at gitub.com/liamhuber/pyspreads.
        """
        self.screen = widgets.HTML(
            value='<style>p{word-wrap: break-word}</style> <p>' + content + ' </p>'
        )
