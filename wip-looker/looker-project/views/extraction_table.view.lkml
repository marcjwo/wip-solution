view: extraction_table {
  sql_table_name: `@{project_id}.@{dataset_id}.@{table_id}` ;;

  dimension: project_name {
    type: string
    sql: ${TABLE}.project_name ;;
  }

  dimension: policy_number {
    type: string
    sql: ${TABLE}.policy_number ;;
  }

  dimension: construction_team_owners {
    type: string
    sql: ${TABLE}.construction_team_owners ;;
  }

  dimension: policy_design {
    type: string
    sql: ${TABLE}.policy_design ;;
  }

  dimension: project_code {
    type: string
    sql: ${TABLE}.project_code ;;
  }

  dimension: project_country {
    type: string
    sql: ${TABLE}.project_country ;;
  }

  dimension: class_of_insurance {
    type: string
    sql: ${TABLE}.class_of_insurance ;;
  }

  dimension: insurerpolicy_or_endorsement {
    type: string
    sql: ${TABLE}.insurerpolicy_or_endorsement ;;
  }

  dimension: limit_currency {
    type: string
    sql: ${TABLE}.limit_currency ;;
  }

  dimension: premium_currency {
    type: string
    sql: ${TABLE}.premium_currency ;;
  }

  dimension: file_location {
    type: string
    sql: ${TABLE}.file_location ;;
  }

  dimension_group: effective_date {
    type: time
    timeframes: [raw, date, month, year, quarter_of_year]
    sql: ${TABLE}.effective_date ;;
  }

  dimension_group: expiry_date {
    type: time
    timeframes: [raw, date, month, year, quarter_of_year]
    sql: ${TABLE}.expiry_date ;;
  }

  dimension: policy_limit_local {
    type: number
    sql: ${TABLE}.policy_limit_local ;;
  }

  dimension: gross_premium_local {
    type: number
    sql: ${TABLE}.gross_premium_local ;;
  }

  dimension: net_premium_local {
    type: number
    sql: ${TABLE}.net_premium_local ;;
  }

  dimension: commission_rate {
    type: number
    sql: ${TABLE}.commission_rate ;;
  }

  dimension: tax_ratefee_local {
    type: number
    sql: ${TABLE}.tax_ratefee_local ;;
  }

  dimension: commission_amount_local {
    type: number
    sql: ${TABLE}.commission_amount_local ;;
  }
}