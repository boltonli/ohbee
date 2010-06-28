
package ob.webapp.rpc;

import java.io.IOException;
import java.util.Vector;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import ob.webapp.rpc.MobileDeviceInfo;
import ob.webapp.rpc.MobileDeviceList;

import org.apache.log4j.Logger;
import org.springframework.web.servlet.ModelAndView;
import equip2.core.IDataspace;
import equip2.core.ISession;
import equip2.core.QueryTemplate;


import equip2.naming.InitialContext;
import equip2.naming.NamingException;

import equip2.core.objectsupport.IObjectHelperRegistry;

import equip2.core.marshall.impl.DefaultContext;
import equip2.core.marshall.impl.JSONUnmarshallRegistry;

import java.io.*;

import ob.webapp.db.*;
import ob.webapp.controller.StateController;

public class MobileUploadController
{
	static Logger logger = Logger.getLogger(MobileUploadController.class.getName());

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
	
	public ModelAndView mobile_list(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_ONLY);
		
		MobileDeviceList mdl = new MobileDeviceList();
		Vector<MobileDeviceInfo> infos = new Vector<MobileDeviceInfo>();
		
		QueryTemplate qt = new QueryTemplate(Metadata.class);
		qt.addConstraintIsNull("parentID");
		qt.addConstraintIsNull("tagID");
		
		Object [] devices = session.match(qt);
		
		for(int i=0; i<devices.length; i++)
		{
			Metadata d = (Metadata) devices[i];
			MobileDeviceInfo mdi = new MobileDeviceInfo();
			mdi.setID(d.getID());
			
			if(d.isSetName() && d.getName().length()!=0)
			{
				mdi.setName(d.getName());				
			}
			else
			{
				mdi.setName("unnamed device");				
			}
						
			infos.add(mdi);
		}

		session.end();
		
		mdl.setDevices(infos.toArray(new MobileDeviceInfo[infos.size()]));
		
		ModelAndView mav = new ModelAndView();
		mav.setView(new EquipObjectView());
		mav.getModel().put(Constants.OBJECT_MODEL_NAME, mdl);

		return mav;
	}
	
	public ModelAndView mobile_test(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		ob.webapp.rpc.MobileUpload mu = new ob.webapp.rpc.MobileUpload();
		mu.setLocation(new Location());
		mu.setSensorData(new ob.webapp.rpc.SensorData());
		mu.setID("blah");
		
		ModelAndView mav = new ModelAndView();
		mav.setView(new EquipObjectView());
		mav.getModel().put(Constants.OBJECT_MODEL_NAME, mu);

		return mav;		
	}
	
	public ModelAndView mobile_upload(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
		String upload = request.getParameter("upload");
		
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
		
		if(!(object instanceof ob.webapp.rpc.MobileUpload))
		{
			response.sendError(HttpServletResponse.SC_BAD_REQUEST, "object is not a MobileUpload");
			return null;			
		}
		
		ob.webapp.rpc.MobileUpload mu = (ob.webapp.rpc.MobileUpload) object;
		
		ISession session = dataspace.getSession();
		session.begin(ISession.READ_ONLY);
		
		Metadata device = (Metadata) session.get(Metadata.class, mu.getID());
		
		if(device==null)
		{
			session.end();
			response.sendError(HttpServletResponse.SC_BAD_REQUEST, "cannot find device " + mu.getID());
			return null;
		}
		
		session.end();
		
		stateController.setLocation(mu.getID(), mu.getLocation());

		response.sendError(HttpServletResponse.SC_OK);
		return null;
	}

}