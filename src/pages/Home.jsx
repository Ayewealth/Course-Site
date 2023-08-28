import React, { useContext, useEffect, useState } from 'react'

import Navbar from '../components/Nav/Navbar'
import Footer from '../components/Footer/Footer'
import AuthContext from '../context/AuthContext'


const Home = () => {
  const { loginMsg } = useContext(AuthContext)
  const [isVisble, setIsVisible] = useState(true)

  useEffect(() => {
    if (loginMsg) {
      const timout = setTimeout(() => {
        setIsVisible(false)
      }, 2000)

      return () => {
        clearTimeout(timout);
      };
    }
  }, [loginMsg])
  return (
    <>
      <Navbar />
      <Footer />
      {isVisble && <p>{loginMsg}</p>}
    </>
  )
}

export default Home