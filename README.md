# Technical Analysis Trading Project

This project consists in simulation and modeling of trading
strategies with technical analysis for 2 tickers with 1 minute time
frame for each: 
* **APPLE** train for 5 min
*  **BITCOIN** train for 5 min
* and their respective test data set for both.

### Tecnhical Indicators
> The techincal indicators used for this project where:
> * RSI
> * BOLL
> * MACD
> * ADX 
> * SMA
> 
> for a total of 31 possible strategies.

With this TIs the team created **BUY** and **SELL** signals for both long positions and short positions.

Then the code checked which indicators were used in the best combination,
 also it reviewed if there was enough capital to create a position, if not the position 
was not executed until there was sufficient capital.

The goal for this project is to obtain the best combination of technical indicators
and get the best parameters and put them into test.

To obtain the best result the team made a for loop, to get all the possible combinations
then the code pass through an optimization process, where the best params and the best combination
are obtained. 

With this result, we try the params in the test dataset and compare the results in a plot
with a **Benchmark** which is a portfolio with the a passive strategy of AAPL/BTC stocks bought with
the starting capital. This is made to have a visual of which strategy performed better.


# Instructions for __ main __.py
In 
>__ main __.py

The user will choose which dataset
will be executed and put your path to get to the data.

* 1.Aple 5 min window
* 2.Bitcoin 5 min window


The main script defines an optimization routine using Optuna to maximize the final capital based on combinations of technical indicators. To run the optimization, execute the code:

> Run |>



# Trading Strategy Project

## Description

## Project Structure

- **data/**: Contains training and test datasets for different timeframes.
- **TA.py/**: Module-specific code to run the strategy.
- **Report.ipynb**: Jupyter notebook containing visualizations, tables, and conclusions.
- **README.md**: Description of the project and instructions to run the main code.
- **requirements.txt**: Libraries and versions required to run the module.
## Usage

## Requirements
- Python 3.10 or higher
- Libraries listed in `requirements.txt`

## Authors
- Rania Aguirre
- Edson Oronia
- Ramon Castañeda



```python

```
