import { Link } from 'react-router-dom'
import { useState } from 'react'
import { useContext } from 'react'

import '../Nav/nav.css'
import ThemeToggle from '../ThemeToggle';
import AuthContext from '../../context/AuthContext'

const Navbar = () => {
    const [removeMenu, setShowMenu] = useState('remove-menu')
    const toggleRemoveMenu = () => {
        setShowMenu((curr) => (curr === "nav__menu" && "remove-menu"))
    }
    const toggleShowMenu = () => {
        setShowMenu((curr) => (curr === "remove-menu" && "nav__menu"))
    }

    let { user, logoutUser } = useContext(AuthContext)

    return (
        <header className='header'>
            <nav className='nav container'>
                <div className="nav__toggle" onClick={toggleShowMenu}>
                    <i className="uil uil-apps"></i>
                </div>
                <div className='nav__logo'>
                    <Link to="/">OpenMinds</Link>
                </div>
                <div className={`nav__menu ${removeMenu}`}>
                    <i className="uil uil-times nav__close" id="nav-close" onClick={toggleRemoveMenu}></i>
                    <ul className='nav__list grid'>
                        <li>
                            <Link className='nav__link' to="/">Home</Link>
                        </li>
                        <li>
                            <Link className='nav__link' to="/about">About</Link>
                        </li>
                        <li>
                            <Link className='nav__link' to="/courses">Courses</Link>
                        </li>
                        <li>
                            <Link className='nav__link' to="/blog">Blog</Link>
                        </li>
                    </ul>
                </div>
                <div className='nav__btns'>
                    <ThemeToggle />

                    <div className='nav__right'>
                        <Link to="/cart"><i className="uil uil-shopping-cart-alt cart"></i></Link>
                        {user ? (
                            <div className='user'>
                                <button onClick={logoutUser}>Logout</button>
                                {user &&
                                    <div>
                                        <p>{user.username}</p>
                                    </div>
                                }
                            </div>
                        ) : (

                            <div className='nav__auth'>
                                <Link to="/login">Signin</Link>
                                <button>
                                    <Link to="/choice">Register</Link>
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </nav>
        </header >
    )
}

export default Navbar