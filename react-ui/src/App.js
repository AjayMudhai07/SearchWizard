import './App.css';
import NavBar from './NavBar';
import Header from './Header';
import Dashboard from './Dashboard';
import MainComponent from './MainComponent';
import ImageGrid from './ImageGrid';
import { useState, useEffect } from 'react';
import HomePage from './HomePage';
import HomePage2 from './HomePage2';

const App = () => {
  const [navItems, setNavItems] = useState([]);
  useEffect(() => {
    fetch("http://127.0.0.1:5000/get_left_nav_items")
        .then(response => response.json())
        .then(data => setNavItems(data))
        .catch(error => console.error("Error fetching left nav items:", error));
}, []);  

const images = [
  "/graph-1.png",
  "/graph-2.png",
  "/graph-3.png",
  "/graph-4.png",
  "/graph-5.png",
  "/graph-6.png",
  "/graph-7.png",
  "/graph-8.png",
];

// console.log(navItems);
// console.log(navItems[0]);

const [isDataSourceSelected, setDataSourceSelected] = useState(false);

return (
  <div className="app-container">
      <NavBar onSelectDataSource={() => setDataSourceSelected(true)} />
      <div className="content">
        <Header />
        {isDataSourceSelected ? <ImageGrid images={images} /> : <HomePage2 />}
      </div>
  </div>
);
}

export default App;

