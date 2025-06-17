import { Link } from 'react-router-dom'
import { ShieldCheckIcon } from '@heroicons/react/24/outline'

export default function Navbar() {
  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex">
            {/* Logo */}
            <Link to="/" className="flex items-center">
              <ShieldCheckIcon className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">
                FakeNewsGuard
              </span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center">
            <Link
              to="/"
              className="px-3 py-2 text-gray-600 hover:text-primary-600"
            >
              Home
            </Link>
            <Link
              to="/admin"
              className="ml-4 px-3 py-2 text-gray-600 hover:text-primary-600"
            >
              Admin
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
