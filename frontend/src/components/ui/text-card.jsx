import PropTypes from 'prop-types';

const TextCard = ({ role, index, children, ...props }) => (
  <div
    {...(index !== undefined && index !== null ? { key: index } : {})}
    className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'}`}
    {...props}
  >
    {role === 'gpt' && (
      <div className="w-2 h-2 mt-2 mr-2 rounded-full bg-emerald-500" />
    )}
    <div
      className={`max-w-[80%] rounded-2xl px-5 py-3.5 ${
        role === 'user'
          ? 'bg-blue-600 text-white shadow-md'
          : 'bg-white text-gray-800 shadow-md border border-gray-100'
      }`}
    >
      {children}
    </div>
  </div>
);

TextCard.displayName = 'TextCard';
TextCard.propTypes = {
  index: PropTypes.number,
  role: PropTypes.oneOf(['user', 'gpt']).isRequired,
  children: PropTypes.node,
};

export { TextCard };
