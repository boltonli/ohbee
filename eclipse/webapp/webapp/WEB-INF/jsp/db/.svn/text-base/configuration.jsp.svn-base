<%@page import="java.util.Map.Entry"%>
<%@ page import="java.util.*" %>
<%@ page import="equip2.core.objectsupport.IStructuredObjectHelper" %>
<%@ page import="equip2.core.objectsupport.IObjectHelper" %>
<%@ page import="equip2.core.objectsupport.IObjectHelperRegistry" %>
<%@ page import="equip2.core.objectsupport.IElement" %>
<%@ page import="equip2.naming.InitialContext" %>
<%@ page import="equip2.spring.PropertyGroupBean" %>
<%@ page import="equip2.spring.EnumTypeBean" %>
<%@ page import="equip2.spring.LinkedClassBean" %>
<%@ page import="org.apache.log4j.Logger" %>

<%!
static Logger logger = Logger.getLogger("equip2.db.jsp.configuration");
static List<String> _allClassNames;
static Map<String, Map<String, String>> _arrayValuedProperties;
static Map<String, Map<String, String>> _maxLengthProperties;
static Map<String, Map<String, String>> _textAreaProperties;
static Map<String, String[]> _listProperties;
static Map<String, Map<String, String>> _niceNames;
static Map<String, Map<String, String>> _niceListHeadings;
static Map<String, LinkedClassBean[]> _linkedClasses;
static Map<String, Map<String, String>> _setValuedProperties;
static Map<String, Map<String, String>> _fixedProperties;
static Map<String, String> _defaultFixedProperties;
static Map<String, PropertyGroupBean[]> _propertyGroups;
static Map<String, PropertyGroupBean> _otherProperties;
static Map<String, Map<String, EnumTypeBean[]>> _enumProperties;
static Map<String, Map<String, EnumTypeBean[]>> _bitFlagProperties;

static {
    
    _allClassNames = new ArrayList<String>();
    _allClassNames.add("ob.webapp.db.Annotation");
_allClassNames.add("ob.webapp.db.Camera");
_allClassNames.add("ob.webapp.db.Location");
_allClassNames.add("ob.webapp.db.Person");
_allClassNames.add("ob.webapp.db.Tag");

    
    _arrayValuedProperties = new HashMap<String, Map<String, String>>();
    
    
    _maxLengthProperties = new HashMap<String, Map<String, String>>();
    _maxLengthProperties.put("ob.webapp.db.Camera", makeMap2(new String[] {"parentID", "null", "ID", "null", "tagID", "null"}));
_maxLengthProperties.put("ob.webapp.db.Annotation", makeMap2(new String[] {"parentID", "null", "ID", "null", "tagID", "null"}));
_maxLengthProperties.put("ob.webapp.db.Tag", makeMap2(new String[] {"ID", "null"}));
_maxLengthProperties.put("ob.webapp.db.Person", makeMap2(new String[] {"parentID", "null", "ID", "null", "tagID", "null"}));

    
    _textAreaProperties = new HashMap<String, Map<String, String>>();
    
    
    _listProperties = new HashMap<String, String[]>();
    
    
    _niceNames = new HashMap<String, Map<String, String>>();
    _niceNames.put("ob.webapp.db.Camera", makeMap2(new String[] {"cameraTiltMinimum", "Tilt Maximum", "cameraPan", "Camera Pan", "location", "Location", "cameraZoomMinimum", "Zoom Minimum", "cameraTilt", "Camera Tilt", "cameraPanMaximum", "Pan Maximum", "cameraZoom", "Camera zoom", "cameraPanMinimum", "Pan", "cameraZoomMaximum", "Zoom Maximum", "url", "Streaming URL", "cameraTiltMaximum", "Tilt Minimum"}));
_niceNames.put("ob.webapp.db.Annotation", makeMap2(new String[] {"location", "Location"}));
_niceNames.put("ob.webapp.db.Location", makeMap2(new String[] {"roll", "Roll", "time", "Time", "altitude", "Altitude", "elevation", "Elevation", "horizontalAccuracy", "Horizontal Accuracy", "longitude", "Longitude", "verticalAccuracy", "Vertical Accuracy", "latitude", "Latitude", "heading", "Heading"}));
_niceNames.put("ob.webapp.db.Person", makeMap2(new String[] {"location", "Location"}));

    
    _niceListHeadings = new HashMap<String, Map<String, String>>();
    
    
    _linkedClasses = new HashMap<String, LinkedClassBean[]>();
    
    
    _setValuedProperties = new HashMap<String, Map<String, String>>();
    

    _fixedProperties = new HashMap<String, Map<String, String>>();
    
    
    _defaultFixedProperties = new HashMap<String, String>();
    _defaultFixedProperties.put("ID", "ID");
        
    _propertyGroups = new HashMap<String, PropertyGroupBean[]>();
    

	_otherProperties = new HashMap<String, PropertyGroupBean>();
    
    for(Map.Entry<String, PropertyGroupBean> entry : _otherProperties.entrySet()) {
        if(_propertyGroups.containsKey(entry.getKey())) {
            PropertyGroupBean[] beans = _propertyGroups.get(entry.getKey());
            PropertyGroupBean[] newBeans = new PropertyGroupBean[beans.length + 1];
            System.arraycopy(beans, 0, newBeans, 0, beans.length);
            newBeans[beans.length] = entry.getValue();
            _propertyGroups.remove(entry.getKey());
            _propertyGroups.put(entry.getKey(), newBeans);
        }
        else
            _propertyGroups.put(entry.getKey(), new PropertyGroupBean[] { entry.getValue() });
    }

	_enumProperties = new HashMap<String, Map<String, EnumTypeBean[]>>();
	HashMap<String, EnumTypeBean[]> ob_webapp_db_CameraEnumGroups = new HashMap<String, EnumTypeBean[]>();
_enumProperties.put("ob.webapp.db.Camera", ob_webapp_db_CameraEnumGroups);
HashMap<String, EnumTypeBean[]> ob_webapp_db_AnnotationEnumGroups = new HashMap<String, EnumTypeBean[]>();
_enumProperties.put("ob.webapp.db.Annotation", ob_webapp_db_AnnotationEnumGroups);
HashMap<String, EnumTypeBean[]> ob_webapp_db_LocationEnumGroups = new HashMap<String, EnumTypeBean[]>();
_enumProperties.put("ob.webapp.db.Location", ob_webapp_db_LocationEnumGroups);
HashMap<String, EnumTypeBean[]> ob_webapp_db_TagEnumGroups = new HashMap<String, EnumTypeBean[]>();
_enumProperties.put("ob.webapp.db.Tag", ob_webapp_db_TagEnumGroups);
HashMap<String, EnumTypeBean[]> ob_webapp_db_PersonEnumGroups = new HashMap<String, EnumTypeBean[]>();
_enumProperties.put("ob.webapp.db.Person", ob_webapp_db_PersonEnumGroups);


	_bitFlagProperties = new HashMap<String, Map<String, EnumTypeBean[]>>();
	HashMap<String, EnumTypeBean[]> ob_webapp_db_CameraBitFlags = new HashMap<String, EnumTypeBean[]>();
_bitFlagProperties.put("ob.webapp.db.Camera", ob_webapp_db_CameraBitFlags);
HashMap<String, EnumTypeBean[]> ob_webapp_db_AnnotationBitFlags = new HashMap<String, EnumTypeBean[]>();
_bitFlagProperties.put("ob.webapp.db.Annotation", ob_webapp_db_AnnotationBitFlags);
HashMap<String, EnumTypeBean[]> ob_webapp_db_LocationBitFlags = new HashMap<String, EnumTypeBean[]>();
_bitFlagProperties.put("ob.webapp.db.Location", ob_webapp_db_LocationBitFlags);
HashMap<String, EnumTypeBean[]> ob_webapp_db_TagBitFlags = new HashMap<String, EnumTypeBean[]>();
_bitFlagProperties.put("ob.webapp.db.Tag", ob_webapp_db_TagBitFlags);
HashMap<String, EnumTypeBean[]> ob_webapp_db_PersonBitFlags = new HashMap<String, EnumTypeBean[]>();
_bitFlagProperties.put("ob.webapp.db.Person", ob_webapp_db_PersonBitFlags);

}

static Map<String, String> makeMap(String[] ss)
{
	Map<String, String> map = new HashMap<String, String>();
	for (int i = 0; i < ss.length; i++)
		map.put(ss[i], ss[i]);
	return map;
}

static Map<String, String> makeMap2(String[] ss)
{
	Map<String, String> map = new HashMap<String, String>();
	for (int i = 0; i < ss.length; i += 2)
		map.put(ss[i], ss[i + 1]);
	return map;
}

static Map<String, String> makeMap(String[] ss, String[] ss2)
{
	Map<String, String> map = new HashMap<String, String>();
	for (int i = 0; i < ss.length; i++)
		map.put(ss[i], ss2[i]);
	return map;
}
%>
<%
	request.setAttribute("allclassnames", _allClassNames.toArray(new String[0]));
	Object requestobject = request.getAttribute("requestobject");
	if (requestobject != null && !(requestobject instanceof equip2.core.QueryTemplate))
	{
		String classname = requestobject.getClass().getName();
		request.setAttribute("listpropertynames", _listProperties.get(classname));
		request.setAttribute("alllistpropertynames", _listProperties);
		request.setAttribute("linkedclasses", _linkedClasses.get(classname));
		request.setAttribute("setvaluedpropertynames", _setValuedProperties.get(classname));
		request.setAttribute("arrayvaluedpropertynames", _arrayValuedProperties.get(classname));
		request.setAttribute("enumproperties", _enumProperties.get(classname));
		request.setAttribute("allenumproperties", _enumProperties);
		request.setAttribute("bitflagproperties", _bitFlagProperties.get(classname));
		request.setAttribute("allbitflagproperties", _bitFlagProperties);
		request.setAttribute("nicenames", _niceNames.get(classname));
		request.setAttribute("allnicenames", _niceNames);
		request.setAttribute("nicelistheadings", _niceListHeadings.get(classname));
		request.setAttribute("allnicelistheadings", _niceListHeadings);
		request.setAttribute("maxlengthproperties", _maxLengthProperties.get(classname));
		request.setAttribute("textareaproperties", _textAreaProperties.get(classname));
        
		if (_fixedProperties.containsKey(classname)) request.setAttribute("fixedpropertynames",
				_fixedProperties.get(classname));
		else
			request.setAttribute("fixedpropertynames", _defaultFixedProperties);

		PropertyGroupBean[] propertygroups = (PropertyGroupBean[]) _propertyGroups.get(classname);
		request.setAttribute("propertygroups", propertygroups);

		PropertyGroupBean otherProperties = (PropertyGroupBean) _otherProperties.get(classname);
		if (otherProperties == null)
		{
			synchronized (_otherProperties)
			{
				otherProperties = new PropertyGroupBean("Other properties");
				Set<String> v = new TreeSet<String>();
				Class<?> clazz = null;
				try
				{
					clazz = Class.forName(classname);
				}
				catch (Exception ex)
				{
					logger.error("Loading class " + classname, ex);
				}
				IObjectHelperRegistry registry = null;
				try
				{
					registry = (IObjectHelperRegistry) (new InitialContext()
							.lookup(IObjectHelperRegistry.JNDI_DEFAULT_NAME));
				}
				catch (Exception rnfe)
				{
					logger.error("No object helper registry registered", rnfe);
				}
				IStructuredObjectHelper shelper = (IStructuredObjectHelper) request
						.getAttribute("objecthelper");
				Enumeration<?> ee = shelper.getIElements(requestobject);
				while (ee.hasMoreElements())
				{
					IElement ie = (IElement) ee.nextElement();
					String pname = ie.getKey().toString();
					boolean found = false;
					if (clazz != null && registry != null && pname.length() > 0
							&& Character.isLetter(pname.charAt(0)))
					{
						String getterName = "get" + Character.toUpperCase(pname.charAt(0)) + pname.substring(1);
						try
						{
							java.lang.reflect.Method m = clazz.getDeclaredMethod(getterName, new Class[0]);
							Class<?> rc = m.getReturnType();
							IObjectHelper phelper = registry.getClassHelper(rc);
							if (phelper instanceof IStructuredObjectHelper
									&& !java.util.Date.class.isAssignableFrom(rc)
									&& !(phelper instanceof equip2.core.objectsupport.impl.ArrayObjectHelper))
							{
								IStructuredObjectHelper sphelper = (IStructuredObjectHelper) phelper;
								Object pv = null;
								try
								{
									pv = rc.newInstance();
									Enumeration<?> ee2 = sphelper.getIElements(pv);
									while (ee2.hasMoreElements())
									{
										IElement ie2 = (IElement) ee2.nextElement();
										String pname2 = pname + "." + ie2.getKey().toString();
										boolean found2 = false;
										for (int i = 0; !found && propertygroups != null
												&& i < propertygroups.length; i++)
											for (int j = 0; !found
													&& j < propertygroups[i].getProperties().length; j++)
												if (pname2.equals(propertygroups[i].getProperties()[j])) found2 = true;

										if (!found2)
										{
											v.add(pname2);
										}
									}
									continue;

								}
								catch (Exception nie)
								{
									logger.error("Could not make template instance of complex property type "
											+ rc, nie);
									continue;
								}
							}
						}
						catch (Exception nsme)
						{
							logger.warn("could not find expected getter method " + getterName + " for class "
									+ classname + " property " + pname, nsme);
						}
					}
					for (int i = 0; !found && propertygroups != null && i < propertygroups.length; i++)
						for (int j = 0; !found && j < propertygroups[i].getProperties().length; j++)
							if (pname.equals(propertygroups[i].getProperties()[j])) found = true;

					if (!found)
					{
						v.add(pname);
					}
				}
				otherProperties.setProperties((String[]) v.toArray(new String[v.size()]));
				if (v.size() > 0)
				{
					if (propertygroups == null) propertygroups = new PropertyGroupBean[1];
					else
					{
						PropertyGroupBean newpropertygroups[] = new PropertyGroupBean[propertygroups.length + 1];
						for (int i = 0; i < propertygroups.length; i++)
							newpropertygroups[i] = propertygroups[i];
						propertygroups = newpropertygroups;
					}
					propertygroups[propertygroups.length - 1] = otherProperties;
					_propertyGroups.put(classname, propertygroups);
					request.setAttribute("propertygroups", propertygroups);
				}
			}
		}
	}
%>
