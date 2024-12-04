# Cloud Kitchen Order Allocation Optimization

## 📍 Project Overview

This project develops an optimization algorithm for smart order routing in multi-location food delivery services, addressing the critical challenge of efficient kitchen order allocation.

## 🚨 Problem Statement

In cloud kitchen environments, simply routing orders to the nearest facility can lead to:
- Uneven kitchen load
- Increased delivery times
- Reduced customer satisfaction

This solution uses a sophisticated linear programming approach to optimize order allocation across multiple kitchen facilities.

## 💻 Dependencies

- PuLP (Linear Programming)
- NumPy
- Pandas

## 🧮 Mathematical Formulation

The problem is formulated as a binary optimization model with:

Decision Variables: Order allocation to facilities

Objective Function: Minimize total delivery distance.

Constraints: 
 - Ensure complete order allocation
 - Maintain service level agreements
 - Prevent duplicate facility assignments

## 📄 License
MIT License
