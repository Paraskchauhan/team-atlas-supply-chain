import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [backendSuppliers, setBackendSuppliers] = useState([])
  const [backendProducts, setBackendProducts] = useState([])
  const [backendRiskData, setBackendRiskData] = useState([])
  const [backendDashboard, setBackendDashboard] = useState({})
  const [backendSimulation, setBackendSimulation] = useState({})
  const [backendMitigation, setBackendMitigation] = useState({})
  const [backendRecommendations, setBackendRecommendations] = useState([])
  const [backendReliability, setBackendReliability] = useState([])
  useEffect(() => {
  fetch('http://127.0.0.1:8000/suppliers')
    .then((response) => response.json())
    .then((data) => {
      setBackendSuppliers(data)
      console.log('Suppliers from backend:', data)
    })
}, [])
useEffect(() => {
  fetch('http://127.0.0.1:8000/products')
    .then((response) => response.json())
    .then((data) => {
      setBackendProducts(data)
      console.log('Products from backend:', data)
    })
}, [])
useEffect(() => {
  fetch('http://127.0.0.1:8000/risk-analysis')
    .then((response) => response.json())
    .then((data) => {
      setBackendRiskData(data)
      console.log('Risk data from backend:', data)
    })
}, [])

useEffect(() => {
  fetch('http://127.0.0.1:8000/dashboard')
    .then((response) => response.json())
    .then((data) => {
      setBackendDashboard(data)
      console.log('Dashboard data from backend:', data)
    })
}, [])

useEffect(() => {
  fetch('http://127.0.0.1:8000/simulation')
    .then((response) => response.json())
    .then((data) => {
      setBackendSimulation(data)
      console.log('Simulation data from backend:', data)
    })
}, [])
useEffect(() => {
  fetch('http://127.0.0.1:8000/simulation/mitigation')
    .then((response) => response.json())
    .then((data) => {
      setBackendMitigation(data)
      console.log('Mitigation data from backend:', data)
    })
}, [])
useEffect(() => {
  fetch('http://127.0.0.1:8000/recommendations')
    .then((response) => response.json())
    .then((data) => {
      setBackendRecommendations(data)
      console.log('Recommendations from backend:', data)
    })
}, [])
useEffect(() => {
  fetch('http://127.0.0.1:8000/supplier-reliability')
    .then((response) => response.json())
    .then((data) => {
      setBackendReliability(data)
      console.log('Supplier reliability from backend:', data)
    })
}, [])
  const suppliers = [
  {
    name: 'Supplier A',
    component: 'Battery',
    deliveryDelay: 6,
    inventoryDays: 3,
    risk: 'High'
  },
  {
    name: 'Supplier B',
    component: 'Display',
    deliveryDelay: 2,
    inventoryDays: 12,
    risk: 'Low'
  },
  {
    name: 'Supplier C',
    component: 'RAM',
    deliveryDelay: 4,
    inventoryDays: 7,
    risk: 'Medium'
  },
  {
    name: 'Supplier D',
    component: 'Processor',
    deliveryDelay: 1,
    inventoryDays: 15,
    risk: 'Low'
  }
]
const products = [
  {
    name: 'Laptop Pro',
    components: ['Battery', 'Display', 'RAM', 'Processor'],
    productionPerDay: 500
  },
  {
    name: 'Laptop Air',
    components: ['Battery', 'Display', 'RAM', 'Processor'],
    productionPerDay: 300
  },
  {
    name: 'Business Laptop',
    components: ['Battery', 'Display', 'RAM', 'Processor'],
    productionPerDay: 200
  }
]
const getAffectedProducts = (supplier) => {
  return products.filter((product) =>
    product.components.includes(supplier.component)
  )
}
const calculateProductionImpact = (supplier) => {
  const affectedProducts = getAffectedProducts(supplier)

  return affectedProducts.reduce(
    (total, product) => total + product.productionPerDay,
    0
  )
}
const calculateRiskScore = (supplier) => {
  const delayRisk = supplier.deliveryDelay * 10
  const inventoryRisk = Math.max(0, 20 - supplier.inventoryDays)

  const score = Math.min(100, delayRisk + inventoryRisk)

  return score
}
const totalSuppliers = backendDashboard.totalSuppliers || 0
const totalProducts = backendDashboard.totalProducts || 0
const highRiskSuppliers = backendDashboard.highRiskSuppliers || 0
const activeRisks = backendDashboard.activeRisks || 0
const overallNetworkStatus =
  activeRisks === 0
    ? 'Stable'
    : activeRisks === 1
    ? 'Watch'
    : 'At Risk'
  const[page, setPage] = useState('Dashboard')
  const [alternativeActivated, setAlternativeActivated] = useState(false)
  return (
    <div className="app">

      <nav className="navbar">
        <div className="logo">
          TEAM-ATLAS
        </div>

        <div className="nav-links">
          <button onClick={() => setPage('Dashboard')}>Dashboard</button>
          <button onClick={() => setPage('Suppliers')}>Suppliers</button>
          <button onClick={() => setPage('Products')}>Products</button>
          <button onClick={() => setPage('Risk Analysis')}>Risk Analysis</button>
          <button onClick={() => setPage('Simulation')}>Simulation</button>
          <button onClick={() => setPage('Recommendations')}>
  Recommendations
</button>
<button onClick={() => setPage('Supplier Reliability')}>
  Supplier Reliability
</button>
        </div>
      </nav>

      <div className="header">
        <h1>AI Supply-Chain Risk Intelligence</h1>
        <p>
          Monitor suppliers, detect risks, and understand supply-chain impact.
        </p>
      </div>

      <h2 className="dashboard-title">{page}</h2>

      {page === 'Products' && (
  <div className="card">
    <h3>Product Supply Overview</h3>

    {backendProducts.map((product) => (
      <div key={product.name}>
        <h3>{product.name}</h3>

        <p>
          Required Components: {product.components.join(', ')}
        </p>

        <p>
          Production Capacity: {product.productionPerDay} units/day
        </p>

        <hr />
      </div>
    ))}
  </div>
)}
          {page === 'Suppliers' && (
  <div className="card">
    <h3>Supplier Overview</h3>

    {backendSuppliers.map((supplier) => (
      <div key={supplier.name}>
        <p>
          <strong>{supplier.name}</strong> - {supplier.component}
        </p>

        <p>Delivery Delay: {supplier.deliveryDelay} days</p>

        <p>Inventory Coverage: {supplier.inventoryDays} days</p>

        <p>Risk Level: {supplier.risk}</p>

        <hr />
      </div>
    ))}
  </div>
)}

{page === 'Risk Analysis' && (
  <div className="card">
    <h3>Supply-Chain Risk Analysis</h3>

    {backendRiskData.map((supplier) => {
      const riskScore = supplier.riskScore
      const affectedProducts = supplier.affectedProducts
      const productionImpact = supplier.productionImpact

      return (
        <div key={supplier.name}>
          <h3>{supplier.name} - {supplier.component}</h3>

          <p>Delivery Delay: {supplier.deliveryDelay} days</p>

          <p>Inventory Coverage: {supplier.inventoryDays} days</p>

          <p>Risk Score: {riskScore}/100</p>

          <p>Risk Level: {supplier.riskLevel}</p>
          <p>Historical Risk Score: {supplier.historicalRiskScore}/40</p>

<p>Overall Risk Score: {supplier.overallRiskScore}/100</p>

<p>Risk Explanation: {supplier.riskExplanation}</p>
                        <p>Affected Products: {affectedProducts.length}</p>
                        <p>
                          Production Impact: {productionImpact} units/day
                        </p>

              <p>
                Products at Risk: {affectedProducts.join(', ')}
              </p>

          <hr />
        </div>
      )
    })}
  </div>
)}
{page === 'Simulation' && (
  <div className="card">
    <h3>Supply-Chain What-If Simulation</h3>

    <p>
  Scenario: {backendSimulation.supplier} becomes unavailable.
</p>

<p>
  Component affected: {backendSimulation.component}
</p>

{!alternativeActivated ? (
  <>
    <p>
      Expected shortage: {backendSimulation.expectedShortage} units
    </p>

    <p>
      Affected products: {backendSimulation.affectedProducts}
    </p>

    <p>
      Estimated production risk: {backendSimulation.riskLevel}
    </p>

        <button onClick={() => setAlternativeActivated(true)}>
          Activate Alternative Supplier
        </button>
      </>
    ) : (
      <>
        <p>
  Alternative Supplier: {backendMitigation.alternativeSupplier}
</p>

<p>
  {backendMitigation.component} supply restored.
</p>

<p>
  Expected shortage: {backendMitigation.expectedShortage} units
</p>

<p>
  Affected products: {backendMitigation.affectedProducts}
</p>

<p>
  Estimated production risk: {backendMitigation.riskLevel}
</p>
<p>
  Previous risk: {backendMitigation.previousRiskLevel}
</p>

<p>
  Products affected before mitigation: {backendMitigation.previousAffectedProducts}
</p>

        <button onClick={() => setAlternativeActivated(false)}>
          Reset Simulation
        </button>
      </>
    )}
  </div>
)}
{page === 'Recommendations' && (
  <div className="card">
    <h3>AI Risk Recommendations</h3>

    {backendRecommendations.map((item) => (
      <div key={item.supplier}>
        <p>
          <strong>{item.supplier}</strong> — {item.component}
        </p>

        <p>
          Risk Score: {item.riskScore}/100
        </p>

        <p>
          Recommendation: {item.recommendation}
        </p>

        <hr />
      </div>
    ))}
  </div>
)}

      {page === 'Dashboard' && (
  <div className="stats">

    <div className="card">
      <h3>Total Suppliers</h3>
      <p>{totalSuppliers}</p>
    </div>

    <div className="card">
      <h3>High Risk Suppliers</h3>
      <p>{highRiskSuppliers}</p>
    </div>

    <div className="card">
      <h3>Products</h3>
      <p>{totalProducts}</p>
    </div>

    <div className="card">
      <h3>Active Risks</h3>
      <p>{activeRisks}</p>
    </div>
    <div className="card status-card">
  <h3>Highest Supply-Chain Risk</h3>

  <p>
    {backendDashboard.highestRiskSupplier}
  </p>

  <p>
    Risk Score: {backendDashboard.highestRiskScore}/100
  </p>
</div>

  </div>
)}
{page === 'Dashboard' && (
  <div className="card status-card">
    <h3>Current Supply-Chain Status</h3>

    <p>Overall Network Status: {overallNetworkStatus}</p>
    <p>
  {activeRisks === 0
    ? 'No immediate supply-chain risks detected.'
    : `${activeRisks} active supply-chain risk detected. Review recommended actions.`}
</p>
    <p>Suppliers Being Monitored: {totalSuppliers}</p>
    <p>High-Risk Suppliers: {highRiskSuppliers}</p>
    <p>Active Supply Risks: {activeRisks}</p>
  </div>
)}
{page === 'Supplier Reliability' && (
  <div className="card">
    <h3>Supplier Reliability</h3>

    {backendReliability.map((supplier) => (
      <div key={supplier.supplierName}>
        <p>
          <strong>{supplier.supplierName}</strong> — {supplier.component}
        </p>

        <p>
          Delivery Events: {supplier.totalEvents}
        </p>

        <p>
          Average Delay: {supplier.averageDelay} days
        </p>

        <p>
          Delay Rate: {supplier.delayRate}%
        </p>
        <p>
  Historical Risk Score: {
    backendRiskData.find(
      (risk) => risk.name === supplier.supplierName
    )?.historicalRiskScore
  }/40
</p>

        <hr />
      </div>
    ))}
  </div>
)}

    </div>
    
  )
}

export default App