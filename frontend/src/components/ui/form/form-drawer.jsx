import * as React from 'react';
import PropTypes from 'prop-types';

import { useDisclosure } from '@/hooks/use-disclosure';

import { Button } from '../button';
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerTrigger,
  DrawerTitle,
} from '../drawer';

export const FormDrawer = ({
  title,
  children,
  isDone,
  triggerButton,
  submitButton,
}) => {
  const { close, open, isOpen } = useDisclosure();

  React.useEffect(() => {
    if (isDone) {
      close();
    }
  }, [isDone, close]);

  return (
    <Drawer
      open={isOpen}
      onOpenChange={(isOpen) => {
        if (!isOpen) {
          close();
        } else {
          open();
        }
      }}
    >
      <DrawerTrigger asChild>{triggerButton}</DrawerTrigger>
      <DrawerContent className="flex max-w-[800px] flex-col justify-between sm:max-w-[540px]">
        <div className="flex flex-col">
          <DrawerHeader>
            <DrawerTitle>{title}</DrawerTitle>
          </DrawerHeader>
          <div>{children}</div>
        </div>
        <DrawerFooter>
          <DrawerClose asChild>
            <Button variant="outline" type="submit">
              Close
            </Button>
          </DrawerClose>
          {submitButton}
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
};
FormDrawer.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  isDone: PropTypes.bool,
  triggerButton: PropTypes.node.isRequired,
  submitButton: PropTypes.node.isRequired,
};