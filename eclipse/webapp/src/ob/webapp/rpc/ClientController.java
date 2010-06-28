
package ob.webapp.rpc;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.Vector;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import ob.webapp.controller.StateController;

import org.apache.log4j.Logger;
import org.springframework.web.servlet.ModelAndView;

import equip2.core.IDataspace;
import equip2.core.ISession;
import equip2.core.QueryTemplate;
import equip2.core.marshall.impl.DefaultContext;
import equip2.core.marshall.impl.JSONUnmarshallRegistry;
import equip2.core.objectsupport.IObjectHelperRegistry;
import equip2.naming.InitialContext;
import equip2.naming.NamingException;

import ob.webapp.db.*;

public class ClientController
{
	static Logger logger = Logger.getLogger(ClientController.class.getName());

	protected IDataspace dataspace;

	public void setDataspace(IDataspace dataspace)
	{
		this.dataspace = dataspace;
	}

	public IDataspace getDataspace()
	{
		return this.dataspace;
	}
	
	protected StateController stateController;
	
	public StateController getStateController()
	{
		return stateController;
	}

	public void setStateController(StateController stateController)
	{
		this.stateController = stateController;
	}

	public ModelAndView client_get_tags(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_ONLY);
		
		TagList tl = new TagList();
		Vector<Tag> tags = new Vector<Tag>();
		
		QueryTemplate qt = new QueryTemplate(Tag.class);
		
		Object [] ts = session.match(qt);
		
		for(int i=0; i<ts.length; i++)
		{
			Tag t = (Tag) ts[i];			
			tags.add(t);
		}

		session.end();
		
		tl.setTags(tags.toArray(new Tag[tags.size()]));
		
		ModelAndView mav = new ModelAndView();
		mav.setView(new EquipObjectView());
		mav.getModel().put(Constants.OBJECT_MODEL_NAME, tl);

		return mav;	
	}
	
	public ModelAndView client_get_scene(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		String tagID = request.getParameter("tag");		
		
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_ONLY);
		
		Scene scene = new Scene();
		
		Vector<Annotation> annotations = new Vector<Annotation>();
		
		QueryTemplate aqt = new QueryTemplate(Annotation.class);
		
		if(tagID!=null && tagID.length()>0)
		{
			aqt.addConstraintEq("tagID", tagID);
		}
		
		Object [] as = session.match(aqt);
		
		for(int i=0; i<as.length; i++)
		{
			Annotation a = (Annotation) as[i];			
			annotations.add(a);
		}
		
		scene.setAnnotations(annotations.toArray(new Annotation[annotations.size()]));

		Vector<Camera> cameras = new Vector<Camera>();
		
		QueryTemplate cqt = new QueryTemplate(Camera.class);
		
		if(tagID!=null && tagID.length()>0)
		{
			cqt.addConstraintEq("tagID", tagID);
		}
		
		Object [] cs = session.match(cqt);
		
		for(int i=0; i<cs.length; i++)
		{
			Camera c = (Camera) cs[i];			
			cameras.add(c);
		}
		
		scene.setCameras(cameras.toArray(new Camera[cameras.size()]));

		Vector<Person> persons = new Vector<Person>();
		
		QueryTemplate pqt = new QueryTemplate(Person.class);
		
		if(tagID!=null && tagID.length()>0)
		{
			pqt.addConstraintEq("tagID", tagID);
		}
		
		Object [] ps = session.match(pqt);
		
		for(int i=0; i<ps.length; i++)
		{
			Person p = (Person) ps[i];			
			persons.add(p);
		}
		
		scene.setPersons(persons.toArray(new Person[persons.size()]));		
		
		session.end();
				
		ModelAndView mav = new ModelAndView();
		mav.setView(new EquipObjectView());
		mav.getModel().put(Constants.OBJECT_MODEL_NAME, scene);

		return mav;	
	}
	
	public ModelAndView client_set_scene(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		String upload = request.getParameter("upload");
		// FIXME - tag?
		
		if(upload==null || upload.length()==0)
		{
			response.sendError(HttpServletResponse.SC_BAD_REQUEST, "cannot find upload parameter");
			return null;
		}

		InitialContext ctx = new InitialContext();
		IObjectHelperRegistry registry = null;
		
		try
		{
			registry = (IObjectHelperRegistry)ctx.lookup(IObjectHelperRegistry.JNDI_DEFAULT_NAME);
		}
		catch(NamingException e)
		{
			response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "naming exception");
			return null;
		}

        JSONUnmarshallRegistry unmarshallRegistry = new JSONUnmarshallRegistry();
        DefaultContext unmarshallContext = new DefaultContext(registry, unmarshallRegistry);		
		
		ByteArrayInputStream bais = new ByteArrayInputStream(upload.getBytes(Constants.JSON_CHARSET));
		Reader input = new BufferedReader(new InputStreamReader(bais));

        Object object = null;
		
		try
		{
			object = unmarshallContext.unmarshall(input);			
		}
		catch(Exception e)
		{
			response.sendError(HttpServletResponse.SC_BAD_REQUEST, "cannot unmarshall object");
			return null;
		}
		
		if(!(object instanceof ob.webapp.rpc.Scene))
		{
			response.sendError(HttpServletResponse.SC_BAD_REQUEST, "object is not a Scene");
			return null;			
		}
		
		ob.webapp.rpc.Scene s = (ob.webapp.rpc.Scene) object;
		
		if(s.isSetAnnotations())
		{
			for(int i=0; i<s.getAnnotations().length; i++)
			{
				stateController.saveAnnotation(s.getAnnotations()[i]);
			}
		}
		
		if(s.isSetCameras())
		{
			for(int i=0; i<s.getCameras().length; i++)
			{
				stateController.saveCamera(s.getCameras()[i]);
			}
		}
		
		if(s.isSetPersons())
		{
			for(int i=0; i<s.getPersons().length; i++)
			{
				stateController.savePerson(s.getPersons()[i]);
			}
		}

		response.sendError(HttpServletResponse.SC_OK);
		return null;
	}
	
	public ModelAndView client_new_annotation(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		Annotation a = stateController.createAnnotation();
		
		ModelAndView mav = new ModelAndView();
		mav.setView(new EquipObjectView());
		mav.getModel().put(Constants.OBJECT_MODEL_NAME, a);

		return mav;	
	}
	
	public ModelAndView client_new_camera(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		Camera c = stateController.createCamera();
		
		ModelAndView mav = new ModelAndView();
		mav.setView(new EquipObjectView());
		mav.getModel().put(Constants.OBJECT_MODEL_NAME, c);

		return mav;	
	}
	
	public ModelAndView client_new_person(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		Person p = stateController.createPerson();
		
		ModelAndView mav = new ModelAndView();
		mav.setView(new EquipObjectView());
		mav.getModel().put(Constants.OBJECT_MODEL_NAME, p);

		return mav;	
	}	
	
	public ModelAndView client_get_scene_live(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{		
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_ONLY);
		
		Scene scene = new Scene();
		
		Vector<Annotation> annotations = new Vector<Annotation>();
		
		QueryTemplate aqt = new QueryTemplate(Annotation.class);
		aqt.addConstraintIsNull("tagID");
		aqt.addConstraintIsNull("parentID");
		
		Object [] as = session.match(aqt);
		
		for(int i=0; i<as.length; i++)
		{
			Annotation a = (Annotation) as[i];			
			annotations.add(a);
		}
		
		scene.setAnnotations(annotations.toArray(new Annotation[annotations.size()]));

		Vector<Camera> cameras = new Vector<Camera>();
		
		QueryTemplate cqt = new QueryTemplate(Camera.class);
		cqt.addConstraintIsNull("tagID");
		cqt.addConstraintIsNull("parentID");
		
		Object [] cs = session.match(cqt);
		
		for(int i=0; i<cs.length; i++)
		{
			Camera c = (Camera) cs[i];			
			cameras.add(c);
		}
		
		scene.setCameras(cameras.toArray(new Camera[cameras.size()]));

		Vector<Person> persons = new Vector<Person>();
		
		QueryTemplate pqt = new QueryTemplate(Person.class);
		pqt.addConstraintIsNull("tagID");
		pqt.addConstraintIsNull("parentID");
		
		Object [] ps = session.match(pqt);
		
		for(int i=0; i<ps.length; i++)
		{
			Person p = (Person) ps[i];			
			persons.add(p);
		}
		
		scene.setPersons(persons.toArray(new Person[persons.size()]));		
		
		session.end();
				
		ModelAndView mav = new ModelAndView();
		mav.setView(new EquipObjectView());
		mav.getModel().put(Constants.OBJECT_MODEL_NAME, scene);

		return mav;	
	}
}