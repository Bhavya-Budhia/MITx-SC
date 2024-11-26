# Supply Chain Analytics Learning Repository

An interactive educational repository for learning mathematical concepts through practical supply chain and business problems.

## Problem Categories

### 1. Optimization Problems
- **BookWise Distribution**: Warehouse location optimization using linear programming
  - Facility location
  - Cost minimization
  - Coverage constraints

- **BooBoo Interactive**: Bullwhip Effect Analysis and Mitigation
  - Supply chain simulation
  - Demand amplification analysis
  - Mitigation strategies comparison
  - Performance visualization

- **BookWise Interactive**: Book-to-Bill Ratio Analysis
  - Order pattern analysis
  - Performance metrics
  - Trend visualization
  - Optimization strategies

### 2. Inventory Management
- **Basic Concepts**
  - ABC Analysis
  - Economic Order Quantity (EOQ)
  - Safety Stock Calculation
  - Reorder Point Determination

- **Advanced Topics**
  - Multi-product Systems
  - Service Level Optimization
  - Cost Trade-off Analysis
  - Dynamic Inventory Models

### 3. Probability and Risk Analysis
- **GameStop Pre-order Analysis**: Video game pre-order optimization
  - Demand modeling
  - Distribution fitting
  - Inventory optimization
  - Risk assessment
  - Monte Carlo simulation

- **Supply Chain Risk Analysis**
  - Bullwhip effect quantification
  - Demand uncertainty modeling
  - Service level probability
  - Risk mitigation strategies

### 4. Statistics and Forecasting
- **SunGlass Hut Inventory**: Apply normal distribution to retail inventory
  - Service level analysis
  - Z-score calculations
  - Two-stage inventory systems

- **QuickPrint Optimization**: Process improvement through hypothesis testing
  - T-tests
  - P-value interpretation
  - Performance metrics

## Repository Structure

```
MITx-SC/
├── inventory_management/
│   ├── basic/
│   │   ├── abc_analysis.ipynb
│   │   ├── eoq_analysis.ipynb
│   │   ├── safety_stock_analysis.ipynb
│   │   └── reorder_point_analysis.ipynb
│   └── advanced/
├── optimization/
│   ├── booboo_interactive.ipynb
│   ├── bookwise_interactive.ipynb
│   └── solutions/
├── probability/
│   ├── gamestop_preorder.ipynb
│   └── solutions/
└── statistics/
    ├── sunglass_hut.ipynb
    └── quickprint.ipynb
```

## Learning Path Structure
Each notebook follows a consistent 4-part learning approach:
1. Concept Introduction and Business Context
2. Mathematical Foundation and Theory
3. Implementation and Code Examples
4. Analysis and Interpretation

## Features
- Interactive Jupyter notebooks
- Real-world business scenarios
- Step-by-step solution guidance
- Comprehensive visualizations
- Automated solution verification
- Extension exercises

## Prerequisites
- Python 3.8+
- Jupyter Notebook environment
- Required libraries:
  - NumPy
  - Pandas
  - Matplotlib
  - Seaborn
  - SciPy

## Getting Started
1. Clone the repository
2. Install required dependencies
3. Launch Jupyter Notebook
4. Navigate to desired topic
5. Follow guided exercises

## Contributing
We welcome contributions! Please see our contributing guidelines for details.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- MITx Supply Chain Management Program
- Contributors and reviewers
- Open source community

## Build Status

[![Python Tests](https://github.com/[your-username]/MITx-SC/actions/workflows/python-tests.yml/badge.svg)](https://github.com/[your-username]/MITx-SC/actions/workflows/python-tests.yml)

## Testing

- All problems include automated tests
- Tests run on Python 3.8, 3.9, and 3.10
- Coverage reports available through CodeCov

## Testing Framework

The repository includes a comprehensive testing framework in `utils/testing/`:

### Core Test Modules
- `test_all.py`: Main test runner
- `probability_tests.py`: Basic probability concept tests
- `inventory_tests.py`: Inventory management tests
- `hypothesis_tests.py`: Statistical testing
- `regression_tests.py`: Regression analysis tests

### Optimization Tests
- `test_warehouse_location.py`: Tests for facility location models
- `test_supply_network.py`: Tests for network optimization
- `test_production_optimization.py`: Tests for production planning
- `test_beverageco.py`: Tests for beverage production
- `test_riskshield.py`: Tests for risk management
- `test_greenchain.py`: Tests for sustainable supply chain

### Case Study Tests
- `test_booboo_interactive.py`: Tests for supply chain risk analysis
- `test_bookwise_interactive.py`: Tests for demand forecasting
