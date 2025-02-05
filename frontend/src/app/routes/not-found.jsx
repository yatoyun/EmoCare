import { Link } from '@/components/ui/link';
import { paths } from '@/configs/paths';

const NotFoundRoute = () => {
  return (
    <div className="mt-52 flex flex-col items-center gap-4 text-center">
      <h1 className="text-3xl font-bold">404 - Page Not Found</h1>
      <p className="text-gray-600">Oops! The page you're looking for doesn't exist.</p>
      <Link
        to={paths.login.getHref()}
        replace
        className="mt-4 hover:text-primary-600"
      >
        Return to Login
      </Link>
    </div>
  );
};

export default NotFoundRoute;