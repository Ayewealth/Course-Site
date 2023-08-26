import { Link } from 'react-router-dom'

import '../Footer/footer.css'
import Links from './Links'

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer__bg">
                <div className="footer__container container grid">
                    <div>
                        <h1 className="footer__title">OpenMinds</h1>
                        <span className="footer__subtitle">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut id tortor porta, aliquam quam auctor, viverra nulla. Praesent ipsum metus,</span>
                        <div className="footer__socials">
                            <Link to="https://www.facebook.com/" target="_blank" className="footer__social">
                                <i className="uil uil-youtube"></i>
                            </Link>

                            <Link to="https://www.instagram.com/" target="_blank" className="footer__social">
                                <i className="uil uil-instagram"></i>
                            </Link>

                            <Link to="https://www.twitter.com/" target="_blank" className="footer__social">
                                <i className="uil uil-twitter-alt"></i>
                            </Link>
                        </div>
                    </div>
                    <Links title="Link" link1="Home" link2="About us" link3="Contact" />
                    <Links title="Legal" link1="Terms" link2="Privacy" link3="Licenses" />
                    <Links title="Products" link1="Overview" link2="Course" link3="Pricing" />
                    <Links title="Resources" link1="Blog" link2="Support" />
                </div>
            </div>
        </footer >
    )
}

export default Footer