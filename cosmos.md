# Cosmos DB Domain Knowledge

## Overview
Azure Cosmos DB is a globally distributed, multi-model database service designed for high availability and low latency. It supports multiple data models including document, graph, key-value, and column-family.

## Key Concepts
- **Multi-Model**: Supports SQL API, MongoDB API, Cassandra API, Gremlin API, and Table API.
- **Global Distribution**: Replicate data across multiple Azure regions for low-latency access.
- **Partitioning**: Horizontal scaling through partition keys for efficient data distribution.
- **Consistency Levels**: Five consistency models from strong to eventual for performance trade-offs.
- **RU (Request Units)**: Measure of throughput, used for billing and capacity planning.

## Best Practices
- Choose appropriate partition keys for even data distribution.
- Use the SQL API for most scenarios unless specific requirements dictate otherwise.
- Implement proper indexing strategies to optimize query performance.
- Monitor RU consumption and scale throughput as needed.
- Use change feed for real-time data processing and event-driven architectures.

## Example
```sql
-- Create a container
CREATE CONTAINER users WITH
PARTITION KEY /userId

-- Insert a document
INSERT INTO users (id, userId, name, email)
VALUES ("1", "user123", "John Doe", "john@example.com")

-- Query documents
SELECT * FROM users WHERE users.userId = "user123"
```