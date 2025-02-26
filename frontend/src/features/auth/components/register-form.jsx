import { Link, useSearchParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import { Button } from '@/components/ui/button';
import { useNotifications } from '@/components/ui/notifications-store';
import { Form, Input } from '@/components/ui/form';
import { paths } from '@/configs/paths';
import { useRegister, registerInputSchema } from '@/lib/auth';

export const RegisterForm = ({
  onSuccess,
}) => {
  const { addNotification } = useNotifications();
  const registering = useRegister({
    onSuccess,
    onError: (error) => {
      addNotification({
        type: 'error',
        title: 'Registration Failed',
        message: error?.message || 'Failed to register. Please try again.',
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
          registering.mutate(values);
        }}
        schema={registerInputSchema}
        options={{
          shouldUnregister: true,
        }}
      >
        {({ register, formState }) => (
          <>
            <Input
              type="text"
              label="Name"
              error={formState.errors['name']}
              registration={register('name')}
            />
            <Input
              type="email"
              label="Email Address"
              error={formState.errors['email']}
              registration={register('email')}
            />
            <Input
              type="password"
              label="Password"
              error={formState.errors['password']}
              registration={register('password')}
            />
            <div>
              <Button
                isLoading={registering.isPending}
                type="submit"
                className="w-full"
              >
                Register
              </Button>
            </div>
          </>
        )}
      </Form>
      <div className="mt-2 flex items-center justify-end">
        <div className="text-sm">
          <Link
            to={paths.login.getHref(redirectTo)}
            className="font-medium text-blue-600 hover:text-blue-500"
          >
            Log In
          </Link>
        </div>
      </div>
    </div>
  );
};
RegisterForm.propTypes = {
  onSuccess: PropTypes.func.isRequired,
};
