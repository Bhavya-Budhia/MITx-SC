# Supply Chain Analytics Learning Repository

An interactive educational repository for learning mathematical concepts through practical supply chain and business problems.

## Problem Categories

### 1. Optimization Problems
- **BookWise Distribution**: Warehouse location optimization using linear programming
  - Facility location
  - Cost minimization
  - Coverage constraints

- **BooBoo Magicians**: Resource allocation optimization
  - Party package optimization
  - Resource constraints
  - Profit maximization

- **FashionFlow Network Design**: Fashion retail supply chain optimization
  - Multi-product distribution network
  - Cross-dock operations
  - Seasonal demand planning
  - Cost-efficient routing

- **GameVerse Network Design**: Supply chain network optimization
  - Multi-product flow optimization
  - Consolidation center balancing
  - Capacity constraints
  - Transportation cost minimization

- **GreenChain Network Design**: Sustainable supply chain optimization
  - Multi-modal transportation
  - Carbon emissions tracking
  - Supplier sustainability scoring
  - Environmental impact minimization

### Network Optimization
- **FashionFlow**: Multi-product distribution network optimization
  - Cross-dock operations
  - Seasonal demand planning
  - Cost-efficient routing

- **GameVerse**: Network design for gaming distribution
  - Multi-product flow optimization
  - Consolidation center balancing
  - Capacity constraints

- **GreenChain**: Sustainable supply chain design
  - Multi-modal transportation
  - Carbon emissions tracking
  - Environmental impact minimization

### Production Planning
- **BeverageCo**: Multi-period production planning
  - Seasonal demand patterns
  - Setup costs and times
  - Shelf-life constraints
  - Storage capacity management

- **TechCraft Production**: Multi-period production optimization
  - Resource allocation
  - Capacity constraints
  - Cost optimization

### Risk Management
- **RiskShield**: Supply chain risk optimization
  - Supplier diversification
  - Buffer inventory planning
  - Geographic risk balancing
  - Service level guarantees

### 2. Case Studies
- **YOUKEA Cost Analysis**: Activity-based costing for furniture retail
  - Cost allocation
  - Profitability analysis
  - Strategic recommendations

### 3. Probability
- **GameStop Pre-order Analysis**: Learn probability concepts through video game collector card distribution
  - Basic probability
  - Conditional probability
  - Multiple event probability

- **Booboo Interactive**: Supply chain risk analysis through probability
  - Risk probability calculations
  - Stockout probability
  - Risk boundaries and thresholds

- **Bookwise Interactive**: Book demand forecasting with probability
  - Demand prediction
  - Confidence intervals
  - Multiple confidence levels

### 4. Statistics
- **SunGlass Hut Inventory**: Apply normal distribution to retail inventory management
  - Service level analysis
  - Z-score calculations
  - Two-stage inventory systems

- **QuickPrint Optimization**: Learn hypothesis testing through process improvement
  - T-tests
  - P-value interpretation
  - Statistical power analysis

### 5. Regression
- **CustomFit Prediction**: Apply regression analysis to service time prediction
  - Linear regression
  - Model diagnostics
  - Prediction intervals

## Build Status

[![Python Tests](https://github.com/[your-username]/MITx-SC/actions/workflows/python-tests.yml/badge.svg)](https://github.com/[your-username]/MITx-SC/actions/workflows/python-tests.yml)

## Repository Structure
```
math_problems/
├── optimization/
│   ├── bookwise_interactive.md
│   ├── booboo_interactive.md
│   ├── distribution/
│   ├── network/
│   └── production/
├── case_studies/
│   ├── youkea_interactive.md
│   ├── manufacturing/
│   ├── retail/
│   └── distribution/
├── probability/
│   └── gamestop_preorder.md
│   └── booboo_interactive.md
│   └── bookwise_interactive.md
├── statistics/
│   ├── sunglass_inventory.md
│   └── quickprint_optimization.md
├── regression/
│   └── customfit_prediction.md
├── utils/
│   └── testing/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_all.py
│       └── [test modules]
├── requirements.txt
├── LICENSE
└── .gitignore
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/math_problems.git
cd math_problems
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest utils/testing/test_all.py -v
```

## Problem Structure

Each problem includes:
1. Business context and problem statement
2. Step-by-step solution guidance
3. Code templates
4. Automated solution verification
5. Extension questions
6. Visualization suggestions

## Problem Types and Tools

### Optimization Problems
- Linear Programming (PuLP)
- Mixed Integer Programming
- Network Optimization

### Statistical Analysis
- Probability Theory
- Normal Distribution
- Hypothesis Testing
- Regression Analysis

### Business Analytics
- Cost Accounting
- Resource Allocation
- Production Planning
- Inventory Management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.
