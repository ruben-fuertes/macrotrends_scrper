from db import ConnexionHandler

main_table_query = """
CREATE TABLE macro_trends (
  ticker VARCHAR(12) NOT NULL,
  year SMALLINT NOT NULL,
  quarter_number SMALLINT NOT NULL,
  quarter VARCHAR(6) NOT NULL,
  cash_on_hand BIGINT,
  receivables BIGINT,
  inventory BIGINT,
  pre_paid_expenses BIGINT,
  other_current_assets BIGINT,
  total_current_assets BIGINT,
  property_plant_and_equipment BIGINT,
  long_term_investments BIGINT,
  goodwill_and_intangible_assets BIGINT,
  other_long_term_assets BIGINT,
  total_long_term_assets BIGINT,
  total_assets BIGINT,
  total_current_liabilities BIGINT,
  long_term_debt BIGINT,
  other_non_current_liabilities BIGINT,
  total_long_term_liabilities BIGINT,
  total_liabilities BIGINT,
  common_stock_net BIGINT,
  retained_earnings_accumulated_deficit BIGINT,
  comprehensive_income BIGINT,
  other_share_holders_equity BIGINT,
  share_holder_equity BIGINT,
  total_liabilities_and_share_holders_equity BIGINT,
  net_income_loss BIGINT,
  total_depreciation_and_amortization_cash_flow BIGINT,
  other_non_cash_items BIGINT,
  total_non_cash_items BIGINT,
  change_in_accounts_receivable BIGINT,
  change_in_inventories FLOAT,
  change_in_accounts_payable BIGINT,
  change_in_assets_liabilities BIGINT,
  total_change_in_assets_liabilities BIGINT,
  cash_flow_from_operating_activities BIGINT,
  net_change_in_property_plant_and_equipment BIGINT,
  net_change_in_intangible_assets FLOAT,
  net_acquisitions_divestitures BIGINT,
  net_change_in_short_term_investments BIGINT,
  net_change_in_long_term_investments BIGINT,
  net_change_in_investments_total BIGINT,
  investing_activities_other BIGINT,
  cash_flow_from_investing_activities BIGINT,
  net_long_term_debt BIGINT,
  net_current_debt BIGINT,
  debt_issuance_retirement_net_total BIGINT,
  net_common_equity_issued_repurchased BIGINT,
  net_total_equity_issued_repurchased BIGINT,
  total_common_and_preferred_stock_dividends_paid BIGINT,
  financial_activities_other BIGINT,
  cash_flow_from_financial_activities BIGINT,
  net_cash_flow BIGINT,
  stock_based_compensation BIGINT,
  common_stock_dividends_paid BIGINT,
  revenue BIGINT,
  cost_of_goods_sold FLOAT,
  gross_profit BIGINT,
  research_and_development_expenses FLOAT,
  sg_a_expenses BIGINT,
  other_operating_income_or_expenses BIGINT,
  operating_expenses BIGINT,
  operating_income BIGINT,
  total_non_operating_income_expense BIGINT,
  pre_tax_income BIGINT,
  income_taxes BIGINT,
  income_after_taxes BIGINT,
  other_income FLOAT,
  income_from_continuous_operations BIGINT,
  income_from_discontinued_operations FLOAT,
  net_income BIGINT,
  ebitda BIGINT,
  ebit BIGINT,
  basic_shares_outstanding BIGINT,
  shares_outstanding BIGINT,
  basic_eps FLOAT,
  eps_earnings_per_share FLOAT,
  current_ratio FLOAT,
  long_term_debt_capital FLOAT,
  debt_equity_ratio FLOAT,
  gross_margin FLOAT,
  operating_margin FLOAT,
  ebit_margin FLOAT,
  ebitda_margin FLOAT,
  pre_tax_profit_margin FLOAT,
  net_profit_margin FLOAT,
  asset_turnover FLOAT,
  inventory_turnover_ratio FLOAT,
  receiveable_turnover FLOAT,
  days_sales_in_receivables FLOAT,
  roe_return_on_equity FLOAT,
  return_on_tangible_equity FLOAT,
  roa_return_on_assets FLOAT,
  roi_return_on_investment FLOAT,
  book_value_per_share FLOAT,
  operating_cash_flow_per_share FLOAT,
  free_cash_flow_per_share FLOAT,
   
   PRIMARY KEY (ticker, year, quarter_number)
) DEFAULT CHARSET=utf8mb4
"""

tickers_table_query = """
CREATE TABLE ticker (
    ticker VARCHAR(12) NOT NULL,
    ticker_desc VARCHAR(100),
    PRIMARY KEY (ticker)
    ) DEFAULT CHARSET=utf8mb4
"""

letter_table_query = """
CREATE TABLE letter_combinations (
  letter_combination VARCHAR(3) NOT NULL,
  checked SMALLINT,
  PRIMARY KEY (letter_combination)
  )
"""

if __name__ == '__main__':
    con_han = ConnexionHandler()
    con_han.query_database(main_table_query, query_type='e')
    con_han.query_database(tickers_table_query, query_type='e')
    con_han.query_database(letter_table_query, query_type='e')
