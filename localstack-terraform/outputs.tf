output "products_bucket" {
  value = aws_s3_bucket.products.bucket
}

output "orders_table" {
  value = aws_dynamodb_table.orders.name
}

output "products_table" {
  value = aws_dynamodb_table.products.name
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.http_api.api_endpoint
}

output "create_order_url" {
  value = "${aws_apigatewayv2_api.http_api.api_endpoint}/orders"
}

output "lambda_function_name" {
  value = aws_lambda_function.create_order.function_name
}
