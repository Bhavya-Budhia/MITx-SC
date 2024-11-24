# Inventory Management

Techniques and models for optimal inventory control in supply chains.

## Basic Models

### Economic Order Quantity (EOQ)
Learn how to determine the optimal order quantity that minimizes total inventory costs. The notebook covers:
- Basic EOQ calculation
- Reorder point determination
- Cost analysis and visualization
- Extensions for variable demand

### ABC Analysis
Implement inventory classification using the ABC analysis method:
- Annual dollar volume calculation
- Category assignment
- Policy recommendations
- Multi-criteria extensions

### Safety Stock Determination
Calculate appropriate safety stock levels considering:
- Service level targets
- Variable lead times
- Multiple products
- Cost-service trade-offs

### Reorder Point Calculation
Determine when to place new orders based on:
- Lead time demand
- Service level requirements
- Variable lead times
- Multiple part considerations

## Advanced Topics (Coming Soon)
- Multi-echelon Inventory Optimization
- Vendor Managed Inventory (VMI)
- Risk Pooling Strategies
- Inventory Routing Problems

## Dependencies
- NumPy: Numerical computations
- SciPy: Statistical functions
- Pandas: Data manipulation
- Matplotlib: Visualization
- Seaborn: Enhanced visualization

## Getting Started
1. Install required packages:
   ```bash
   pip install numpy scipy pandas matplotlib seaborn
   ```

2. Navigate to the desired topic directory:
   ```bash
   cd inventory_management/basic
   ```

3. Open the Jupyter notebooks:
   ```bash
   jupyter notebook
   ```

## Testing
Each notebook includes test functions to validate your solutions. The tests check:
- Calculation accuracy
- Parameter reasonableness
- Service level achievement
- Cost optimality

## Contributing
Feel free to contribute by:
1. Adding new inventory management problems
2. Enhancing existing notebooks
3. Improving test coverage
4. Adding real-world case studies

## License
MIT License - See LICENSE file for details
