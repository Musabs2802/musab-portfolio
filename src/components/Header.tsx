import React, { useState, useEffect } from "react";
import { Menu, X } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import site from "../data/site.data";

const navItems = [
  { label: "Services", to: "/#services" },
  { label: "Case Studies", to: "/#case-studies" },
  { label: "Work", to: "/works" },
  { label: "Pricing", to: "/#pricing" },
  { label: "Experience", to: "/experience" },
  { label: "Contact", to: "/contact" },
];

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    handleScroll();
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setIsMenuOpen(false);
  }, [location.pathname, location.hash]);

  const isActive = (to: string) =>
    !to.includes("#") && location.pathname === to;

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled || isMenuOpen
          ? "bg-white/90 backdrop-blur-md shadow-[0_1px_0_rgba(0,0,0,0.06)]"
          : "bg-transparent"
      }`}
    >
      <div className="container-page">
        <div className="flex justify-between items-center h-16">
          <Link
            to="/"
            className="flex items-center gap-2.5 font-heading font-semibold text-ink"
          >
            <img
              src={site.avatar}
              alt=""
              className="w-8 h-8 rounded-full object-cover bg-sand-200"
            />
            Musab Shaikh
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map(({ label, to }) => (
              <Link
                key={to}
                to={to}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive(to)
                    ? "text-brand-800 bg-brand-50"
                    : "text-neutral-600 hover:text-ink hover:bg-sand-200/60"
                }`}
              >
                {label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            <a
              href={site.calendly}
              target="_blank"
              rel="noopener noreferrer"
              className="hidden sm:inline-flex btn-primary !py-2 !px-4"
            >
              Book a free call
            </a>

            {/* Mobile Menu Button */}
            <button
              className="lg:hidden p-2 rounded-lg hover:bg-sand-200 transition text-ink"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Toggle menu"
              aria-expanded={isMenuOpen}
            >
              {isMenuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <nav className="lg:hidden pb-4 border-t border-sand-200 pt-2">
            {navItems.map(({ label, to }) => (
              <Link
                key={to}
                to={to}
                className={`block px-3 py-2.5 rounded-lg text-[15px] ${
                  isActive(to)
                    ? "bg-brand-50 text-brand-800 font-medium"
                    : "text-neutral-700 hover:bg-sand-100"
                }`}
              >
                {label}
              </Link>
            ))}
            <a
              href={site.calendly}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary w-full mt-3 sm:hidden"
            >
              Book a free call
            </a>
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;
