import PropTypes from 'prop-types';

import { Error } from './error';
import { Label } from './label';

export const FieldWrapper = (props) => {
  const { label, error, children } = props;
  return (
    <div>
      <Label>
        {label}
        <div className="mt-1">{children}</div>
      </Label>
      <Error errorMessage={error?.message} />
    </div>
  );
};

FieldWrapper.propTypes = {
  label: PropTypes.string.isRequired,
  error: PropTypes.object,
  children: PropTypes.node,
};