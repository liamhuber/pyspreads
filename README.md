# pyspreads

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Welcome to pyspreads, a small app for playing around with [vertical spreads](https://www.investopedia.com/terms/v/verticalspread.asp) in options trading.

Spin up the Voila instance (it might take a while if the environment needs to be built) and have fun constructing a collection of options positions from the test data (SPY options a few months from expiry), or copy and paste your own data into the app.
It is overall a fairly primitive tool, limited only to vertical options and focused on returns at expiration, without any real consideration of theta decay, delta, etc.

# Objectives

## Pedagogy

I really like the way investopedia and other online resource use graphs to quickly communicate the idea behind options trading strategies, but it always frustrated me that these were (a) static, and (b) using made-up numbers.
Here I wanted to give a tool that allows the user to explore what the return curves for these strategies look like in real life, as well as constructing other strategies -- with the major caveat that this software only supports *vertical* strategies, i.e. those where every position has the same expiry date.

I feel the project was very successful on this front.

## Trading

I have been trading options myself for a while now, but my broker doesn't offer very sophisticated tools, so I wanted something that would provide a more intuitive way of exploring available trades.
Beyond that, I've noticed that there are sometimes minor inefficiencies in the market -- where a particular contract will be priced lower than the contracts with strike prices on *either* side.
So I wanted a tool that would make these inefficiencies easier to spot (without going all the way to automated trading).

On this front I feel the project is actually fairly weak.
At the moment I compare the contract premium (i.e. cost - value, where value is non-zero for in-the-money contracts), and compare actual contract premiums to a smoothed curve to see which are undervalued.
The test data I've been working with, however, displays some discontinuities I don't well understand yet, which wreak havoc with the raw-to-smoothed comparison.
Simply constructing positions went a bit better, and the max return and max drawdown functions are nice.
There is also a computed expectation curve to communicate the market's expectations on price movement as computed by out-of-the-money contract costs.
This is used to compute an expected return for the positions, but shouldn't be taken at all seriously since the underlying model is just the first thing that came to mind.
However, I do think it's at least qualitatively useful for quickly seeing whether the market feels the underlying asset has upwards or downwards momentum as measured by the symmetry of this curve.

## Professional development

I started using ipywidgets professionally earlier this year, so I'm always looking for opportunities to play around with it, try out new architectures, and generally see what can be done.
To that end, I wanted to power through and see what I could crank out in a week's time as an evenings-and-weekends project.

Here I'm also quite happy. 
There are some rough edges, e.g. it's not super efficient, and I didn't get to making the plots interactive, but I hit most of the features I was gunning for at outset.
I might revisit the project in the future if I get more insight into/read more about modeling asset price expectation from options prices, or discover that it's more useful than expected for taking actual options positions.
But for now I'll be content to have this version running on MyBinder.