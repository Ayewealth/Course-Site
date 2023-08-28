import { Link } from 'react-router-dom'

import "../components/Choice/choice.css"

const Choice = () => {
  return (
    <div className='choices'>
      <div className='choice'>
        <div id='link'>
          <Link to="/"><i className="uil uil-arrow-left"></i> Back to home</Link>
        </div>
        <div className='choice__btns'>
          <Link to="/instructor">
            <button>
              Continue as Instructor <i className="uil uil-arrow-up-right"></i>
            </button>
          </Link>
          <Link to="/student">
            <button>
              Continue as Student <i className="uil uil-arrow-up-right"></i>
            </button>
          </Link>
        </div>
        <div id='goal'>
          <p>The Goal - Making Education Easy And Wide Spread</p>
        </div>
      </div>
    </div>
  )
}

export default Choice