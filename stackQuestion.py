class Users(Base):
        __tablename__ = 'users'
        name = Column(String(80), nullable=False)
        email = Column(String(80), nullable=False)
        id = Column(Integer, primary_key=True)
        bio = Column(String(300))
        picture = Column(String(80))
    
    
class Category(Base):
        __tablename__ = 'category'
        name = Column(String(80), nullable=False)
        id = Column(Integer, primary_key=True)
        user = Column(Integer, ForeignKey(Users.id))
        users = relationship(Users)
    
        @property
        def serialize(self):
            return{
                'id': self.id,
                'name': self.name
            }
    
    
class Artisan(Base):
        __tablename__ = 'artisan'
        name = Column(String(80), nullable=False)
        skill = Column(String(80), nullable=False)
        id = Column(Integer, primary_key=True)
        bio = Column(String(300))
        category = Column(Integer, ForeignKey(Category.id))
        user = Column(Integer, ForeignKey(Users.id))
        id_no = Column(Integer, nullable=False)
        users = relationship(Users)
    
        @property
        def serialize(self):
            return{
                'id': self.id,
                'name': self.name,
                'skill': self.skill,
                'category': self.category,
                'bio': self.bio,
                'id_no': self.id_no
    
            }
    
    
class Portfolio(Base):
        __tablename__ = 'portfolio'
        title = Column(String(80), nullable=False)
        details = Column(String(300), nullable=False)
        id = Column(Integer, primary_key=True)
        artisan = Column(Integer, ForeignKey(Artisan.id))
        user = Column(Integer, ForeignKey(Users.id))
        users = relationship(Users)
    
        @property
        def serialize(self):
            return{
                'id': self.id,
                'title': self.title,
                'details': self.details
            }
    
    
class Endorsements(Base):
        __tablename__ = 'endorsements'
        title = Column(String(80), nullable=False)
        details = Column(String(300), nullable=False)
        id = Column(Integer, primary_key=True)
        artisan = Column(Integer, ForeignKey(Artisan.id))
        user = Column(Integer, ForeignKey(Users.id))
        users = relationship(Users)
    
        @property
        def serialize(self):
            return{
                'id': self.id,
                'title': self.title,
                'details': self.details
            }
    
    
class Address(Base):
        __tablename__ = 'address'
        building = Column(String(80), nullable=False)
        floor = Column(String(80), nullable=False)
        house_no = Column(String(80), nullable=False)
        telephone = Column(String(80), nullable=False)
        kwetu_address = Column(String(80), nullable=False)
        id = Column(Integer, primary_key=True)
        lat = Column(String(25))
        lng = Column(String(25))
        artisan = Column(Integer, ForeignKey(Artisan.id))
        user = Column(Integer, ForeignKey(Users.id))
        users = relationship(Users)
    
        @property
        def serialize(self):
            return{
                'id': self.id,
                'lat': self.lat,
                'lng': self.lng,
                'kwetu_address': self.kwetu_address,
                'artisan': self.artisan
            }
    
    
    