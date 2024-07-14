from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _ 

class UtilisateursManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, pseudo, password, **extra_fileds):
        
        if not pseudo:
            raise ValueError('Le pseudo doit être défini')
        pseudo = self.normalize_email(pseudo)
        user = self.model(pseudo=pseudo, **extra_fileds)
        user.set_password(password) # crypte
        user.save(using=self._db)
        return user
    
    def create_user(self, pseudo, password, **extra_fileds):
        extra_fileds.setdefault('is_superuser', False)
        return self.create_user(pseudo, password, **extra_fileds)
    
    def create_superuser(self, pseudo, password, **extra_fileds):
        extra_fileds.setdefault('is_superuser', True)
        extra_fileds.setdefault('is_staff', True)
        extra_fileds.setdefault('is_active', True)
        
        if extra_fileds.get('is_staff') is not True:
            raise ValueError(_('SuperUser doit avoir is_staff =True'))
        if extra_fileds.get('is_superuser') is not True:
            raise ValueError(_('SuperUser doit avoir is_superuser =True'))
        
        return self._create_user(pseudo, password, **extra_fileds)