import * as React from 'react';
import PropTypes from 'prop-types';
import { cn } from '@/utils/cn';

const Container = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8',
      className
    )}
    {...props}
  />
));

Container.displayName = 'Container';
Container.propTypes = {
  className: PropTypes.string,
};

export { Container };
