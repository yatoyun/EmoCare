import { Link as RouterLink } from "react-router-dom";
import PropTypes from "prop-types";

import { cn } from "@/utils/cn";

export const Link = ({ className, children, ...props }) => {
	return (
		<RouterLink
			className={cn("text-slate-600 hover:text-slate-900", className)}
			{...props}
		>
			{children}
		</RouterLink>
	);
};

Link.propTypes = {
	className: PropTypes.string,
	children: PropTypes.node.isRequired,
};
