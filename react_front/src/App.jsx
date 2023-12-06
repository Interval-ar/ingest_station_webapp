
import { Route, Routes } from 'react-router-dom'
import './App.css'
import "./css/header.scss"
import "./css/main.scss"
import "./css/gestion.scss"
import Main_page from './modules/Main_page'
import Header from './modules/header'
import Gestion from './modules/Gestion'
import Config from './modules/Config'

function App() {
  return (
    <>
      <Header></Header>  
      <Routes>
            <Route path="/" element={<Main_page/>}/>
            <Route path="/gestion" element={<Gestion/>}/>
            <Route path="/config" element={<Config/>}/>


       </Routes>
     
    </>
  )
}

export default App
