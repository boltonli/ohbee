
package ob.webapp.rpc;

import org.springframework.web.servlet.View;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import equip2.naming.*;

import equip2.core.objectsupport.IObjectHelperRegistry;
import equip2.core.objectsupport.IStructuredObjectHelper;

import equip2.core.marshall.IMarshallingRegistry;
import equip2.core.marshall.impl.DefaultMarshallAsXmlRegistry;
import equip2.core.marshall.impl.ECMAScriptMarshallRegistry;
import equip2.core.marshall.impl.DefaultContext;
import equip2.core.marshall.impl.JSONMarshallRegistry;

import java.util.Map;

/** Spring controller which handles most of the database view operations via
 * a multi-controller delegation.
 */
public class EquipObjectView implements View
{
    /** cons
     */
    public EquipObjectView() 
    {
    }
    /** render
     */
    public void render(Map model, HttpServletRequest request, HttpServletResponse response) throws Exception 
    {
		response.setHeader("Cache-Control", "no-store");
		response.setHeader("Pragma", "no-cache");
		response.setDateHeader("Expires", 0);
    	
		Object object = model.get(Constants.OBJECT_MODEL_NAME);

		InitialContext ctx = new InitialContext();
		IObjectHelperRegistry registry = (IObjectHelperRegistry)ctx.lookup(IObjectHelperRegistry.JNDI_DEFAULT_NAME);
		IMarshallingRegistry marshallRegistry = null;
		String encoding = request.getParameter(Constants.ENCODING_PARAMETER_NAME);
		boolean includeXmlPrologue = false;
		boolean includeXmlTopLevelElement = false;

		if (Constants.XML_ENCODING.equals(encoding))
		{
		    includeXmlPrologue = true;
		    response.setContentType("text/xml; charset=UTF-8");
		    marshallRegistry = new DefaultMarshallAsXmlRegistry();
		    // special case for non-element XML type
		    if (!(registry.getObjectHelper(object) instanceof IStructuredObjectHelper))
			includeXmlTopLevelElement = true;
		}
		else
		{
		    marshallRegistry = new JSONMarshallRegistry(); //ECMAScriptMarshallRegistry();
		    response.setContentType("text/plain; charset=UTF-8");			
		}
		
		DefaultContext marshallContext = new DefaultContext(registry, marshallRegistry);
	
		java.io.PrintStream writer = new java.io.PrintStream(response.getOutputStream(), false, "UTF-8");
		if (includeXmlPrologue)
		{
			writer.println("<?xml version=\"1.0\"?>");
		}
		if (includeXmlTopLevelElement)
		{
			writer.println("<primitive>");
		}
		marshallContext.marshall(object, writer);
		if (includeXmlTopLevelElement)
		{
			writer.println("</primitive>");
		}
		writer.close();
    }
    
    /** 
     * Necessary for Spring 2.0 compatibility, returns null to show that
     * the content type is not predetermined.
     */
	public String getContentType()
    {
    	return null;
    }
}
