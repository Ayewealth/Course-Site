import { useContext } from 'react'
import { FcGoogle } from 'react-icons/fc'
import { Link } from 'react-router-dom'

import AuthContext from '../../context/AuthContext'


const InstructorForm = () => {
  const { instructorReg } = useContext(AuthContext)

  return (
    <div className='form__div'>
      <div className='left'>
        <div className='left__inner'>
          <h3>
            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 39 39" fill="none">
              <path d="M30.1276 14.625L14.4301 5.62245C13.5807 5.13196 12.6166 4.87501 11.6357 4.87771C10.6549 4.8804 9.69222 5.14264 8.84551 5.63779C7.99881 6.13294 7.29823 6.84336 6.81494 7.69689C6.33165 8.55042 6.08287 9.51665 6.09385 10.4975V28.5674C6.09385 30.0414 6.67938 31.455 7.72161 32.4972C8.76384 33.5394 10.1774 34.125 11.6514 34.125C12.6271 34.1233 13.5852 33.8655 14.4301 33.3775L30.1276 24.3749C30.9711 23.8868 31.6714 23.1854 32.1582 22.3412C32.645 21.4969 32.9013 20.5395 32.9013 19.5649C32.9013 18.5904 32.645 17.633 32.1582 16.7887C31.6714 15.9445 30.9711 15.2431 30.1276 14.755V14.625ZM28.5026 21.4337L12.8051 30.5662C12.4533 30.7656 12.0558 30.8704 11.6514 30.8704C11.2469 30.8704 10.8494 30.7656 10.4976 30.5662C10.1468 30.3636 9.85543 30.0723 9.6529 29.7214C9.45037 29.3706 9.34379 28.9726 9.34386 28.5674V10.4325C9.34379 10.0273 9.45037 9.62934 9.6529 9.27848C9.85543 8.92762 10.1468 8.63626 10.4976 8.4337C10.8509 8.23733 11.2472 8.13127 11.6514 8.12495C12.0552 8.13324 12.4511 8.23917 12.8051 8.4337L28.5026 17.5012C28.8536 17.7037 29.145 17.995 29.3477 18.3459C29.5504 18.6967 29.657 19.0948 29.657 19.4999C29.657 19.9051 29.5504 20.3032 29.3477 20.654C29.145 21.0049 28.8536 21.2962 28.5026 21.4987V21.4337Z" fill="#0092E4" />
            </svg>
            Digital platform for distance <span>learning</span>
          </h3>
          <p>You will never know everything But you will know more.</p>
        </div>
      </div>
      <div className='right'>
        <div className='right__inner'>
          <div className='right__top'>
            <h3>Create your account</h3>
            <button>
              <i><FcGoogle /></i>
              Sign up with Google
            </button>
          </div>
          <div id='or'>
            <span></span>
            Or
            <span></span>
          </div>
          <form onSubmit={instructorReg}>
            <div id='input__field'>
              <label>Instructor name</label>
              <input type="text" name='name' />
            </div>
            <div id='input__field'>
              <label>Username</label>
              <input type="text" name='username' />
            </div>
            <div id='input__field'>
              <label>Email</label>
              <input type="email" name='email' />
            </div>
            <div id='input__field'>
              <label>Password</label>
              <input type="password" name='password' />
            </div>
            <div id='terms'>
              <input type="checkbox" name="checkbox" />
              I agree to all Terms, Privacy Policy
            </div>
            <button type="submit" id='submit__btn'>Sign Up</button>
            <p id='redirect'>Already have an account? <Link to="/login">Login</Link></p>
          </form>
        </div>
      </div>
    </div >
  )
}

export default InstructorForm