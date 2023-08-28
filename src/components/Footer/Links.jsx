import { Link } from 'react-router-dom'

import '../Footer/footer.css'

const Links = ({ title, link1, link2, link3 }) => {
    return (
        <div>
            <ul className="footer__links">
                <h3>{title}</h3>
                <li>
                    <Link to="" className="footer__link">{link1}</Link>
                </li>

                <li>
                    <Link to="" className="footer__link">{link2}</Link>
                </li>

                <li>
                    <Link to="" className="footer__link">{link3}</Link>
                </li>
            </ul>
        </div>
    )
}

export default Links