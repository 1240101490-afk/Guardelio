import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import Button from './Button';

const Pagination = ({
  currentPage = 1,
  totalItems = 0,
  pageSize = 20,
  onPageChange,
  className = '',
}) => {
  const totalPages = Math.ceil(totalItems / pageSize);

  if (totalPages <= 1) return null;

  return (
    <div className={`flex items-center justify-between border-t border-slate-100 px-4 py-3 sm:px-6 ${className}`}>
      <div className="flex flex-1 justify-between sm:hidden">
        <Button
          variant="outline"
          size="sm"
          disabled={currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          disabled={currentPage === totalPages}
          onClick={() => onPageChange(currentPage + 1)}
        >
          Next
        </Button>
      </div>
      <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div>
          <p className="text-xs text-slate-500">
            Showing <span className="font-semibold text-slate-700">{((currentPage - 1) * pageSize) + 1}</span> to{' '}
            <span className="font-semibold text-slate-700">
              {Math.min(currentPage * pageSize, totalItems)}
            </span>{' '}
            of <span className="font-semibold text-slate-700">{totalItems}</span> results
          </p>
        </div>
        <div>
          <nav className="isolate inline-flex -space-x-px rounded-md shadow-xs" aria-label="Pagination">
            <Button
              variant="outline"
              size="sm"
              className="rounded-r-none rounded-l-md px-2 py-2"
              disabled={currentPage === 1}
              onClick={() => onPageChange(currentPage - 1)}
              icon={ChevronLeft}
            />
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                onClick={() => onPageChange(page)}
                className={`relative inline-flex items-center px-4 py-2 text-xs font-semibold focus:z-20 ${
                  page === currentPage
                    ? 'z-10 bg-cyan-600 text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-600'
                    : 'text-slate-900 ring-1 ring-inset ring-slate-200 hover:bg-slate-50 focus:outline-offset-0'
                }`}
              >
                {page}
              </button>
            ))}
            <Button
              variant="outline"
              size="sm"
              className="rounded-l-none rounded-r-md px-2 py-2"
              disabled={currentPage === totalPages}
              onClick={() => onPageChange(currentPage + 1)}
              icon={ChevronRight}
            />
          </nav>
        </div>
      </div>
    </div>
  );
};

export default Pagination;
