
package ob.webapp.controller;

import ob.webapp.rpc.MobileUploadController;

import org.apache.log4j.Logger;

import equip2.core.IDataspace;
import equip2.core.ISession;
import equip2.spring.db.IDAllocator;

import ob.webapp.db.*;

public class StateController
{
	static Logger logger = Logger.getLogger(StateController.class.getName());
	
	protected IDataspace dataspace;

	public IDataspace getDataspace()
	{
		return dataspace;
	}

	public void setDataspace(IDataspace dataspace)
	{
		this.dataspace = dataspace;
	}
	
	public StateController()
	{
		
	}
	
	public void saveAnnotation(Annotation a)
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_WRITE);
		
		if(a.isSetID())
		{
			Annotation da = (Annotation) session.get(Annotation.class, a.getID());
			
			if(da==null)
			{
				a.setID(IDAllocator.getNewID(session, Annotation.class, "A", null));
				session.add(a);
			}
			else
			{
				session.addOrUpdate(a);
			}			
		}
		else
		{
			a.setID(IDAllocator.getNewID(session, Annotation.class, "A", null));
			session.add(a);
		}
		
		session.end();
	}
	
	public void saveCamera(Camera c)
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_WRITE);
		
		if(c.isSetID())
		{
			Camera dc = (Camera) session.get(Camera.class, c.getID());
			
			if(dc==null)
			{
				c.setID(IDAllocator.getNewID(session, Camera.class, "C", null));
				session.add(c);
			}
			else
			{
				session.addOrUpdate(c);
			}			
		}
		else
		{
			c.setID(IDAllocator.getNewID(session, Camera.class, "C", null));
			session.add(c);
		}
		
		session.end();
	}
	
	public void savePerson(Person p)
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_WRITE);
		
		if(p.isSetID())
		{
			Person dp = (Person) session.get(Person.class, p.getID());
			
			if(dp==null)
			{
				p.setID(IDAllocator.getNewID(session, Person.class, "P", null));
				session.add(p);
			}
			else
			{
				session.addOrUpdate(p);
			}			
		}
		else
		{
			p.setID(IDAllocator.getNewID(session, Person.class, "P", null));
			session.add(p);
		}
		
		session.end();
	}
	
	
	public Annotation createAnnotation()
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_WRITE);
		
		Annotation a = new Annotation();
		a.setLocation(new Location());
		a.setID(IDAllocator.getNewID(session, Annotation.class, "A", null));
		session.add(a);
		
		session.end();
		
		return a;
	}
	
	public Camera createCamera()
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_WRITE);
		
		Camera c = new Camera();
		c.setLocation(new Location());
		c.setID(IDAllocator.getNewID(session, Camera.class, "C", null));
		session.add(c);
		
		session.end();
		
		return c;		
	}
	
	public Person createPerson()
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_WRITE);
		
		Person p = new Person();
		p.setLocation(new Location());
		p.setID(IDAllocator.getNewID(session, Person.class, "P", null));
		session.add(p);
		
		session.end();
		
		return p;		
	}
	
	public void setLocation(String deviceID, Location location)
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_WRITE);
		
		Locatable device = (Locatable) session.get(Locatable.class, deviceID);
		
		if(device==null)
		{
			logger.error("setLocation could not find " + deviceID + " to update");
			session.end();
			return;
		}
		
		device.setLocation(location);		
		
		session.end();
	}
	
}