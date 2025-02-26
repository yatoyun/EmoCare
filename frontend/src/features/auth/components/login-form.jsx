import { Link, useSearchParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import { Button } from '@/components/ui/button';
import { useNotifications } from '@/components/ui/notifications-store';
import { Form, Input } from '@/components/ui/form';
import { paths } from '@/configs/paths';
import { useLogin, loginInputSchema } from '@/lib/auth';

export const LoginForm = ({ onSuccess }) => {
  const { addNotification } = useNotifications();
  const login = useLogin({
    onSuccess,
    onError: () => {
      addNotification({
        type: 'error',
        title: 'Login Failed',
        message: 'Login failed',
        duration: 3000
      });
    },
    retry: false,
    useErrorBoundary: false,
  });
  const [searchParams] = useSearchParams();
  const redirectTo = searchParams.get('redirectTo');

  return (
    <div>
      <Form
        onSubmit={(values) => {
          login.mutate(values);
        }}
        schema={loginInputSchema}
        options={{
          shouldUnregister: true,
        }}
      >
        {({ register, formState }) => (
          <>
            <Input
              type="name"
              label="Name"
              error={formState.errors['name']}
              registration={register('name')}
            />
            <Input
              type="password"
              label="Password"
              error={formState.errors['password']}
              registration={register('password')}
            />
            <div>
              <Button
                isLoading={login.isPending}
                type="submit"
                className="w-full"
              >
                Log in
              </Button>
            </div>
          </>
        )}
      </Form>
      <div className="mt-2 flex items-center justify-end">
        <div className="text-sm">
          <Link
            to={paths.register.getHref(redirectTo)}
            className="font-medium text-blue-600 hover:text-blue-500"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  );
};

LoginForm.propTypes = {
  onSuccess: PropTypes.func.isRequired,
};
