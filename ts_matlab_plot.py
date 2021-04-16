function glyphscript(engineState)
	% MATLAB调用需确保 ncode与matlab匹配 如32位对32位,64位对64位
	ts_in1 = engineState.GetInputTimeSeries(1);
	ts_out1 = engineState.GetOutputTimeSeries(1);

	data = get_channel_data(ts_in1);


	set_ouput_ts(ts_out1, ts_in1, data)
	% set_channel_data(ts_out1, data);
	% copy_chanenel_data(ts_out1, ts_in1);

	% 作图
	x_channel = 1;
	y_channel = 2;
	fig_num = 1;
	plot_single(x_channel, y_channel, ts_in1, fig_num, '.r', 111);

end


function set_ouput_ts(ts_obj, ts_obj_source, data)
	
	set_channel_data(ts_obj, data);
	copy_chanenel_data(ts_obj, ts_obj_source);

end

% 获取数据
function data = get_channel_data(ts_obj)

	n_channel = ts_obj.GetChannelCount()
	for i = 1:n_channel
		n_point = ts_obj.GetPointCount(i)
		data(i,:) = ts_obj.GetValues(i, 1, n_point)
	end	
end

% 通道数据赋予
function set_channel_data(ts_obj, data)
	n_channel = length(data(:,1));
	ts_obj.SetChannelCount(n_channel);
	for i = 1:n_channel
		ts_obj.SetPointCount(i, length(data(i,:)));
		ts_obj.PutValues(i, 1, data(i,:));
	end
end

% 复制通道信息
function ts_obj = copy_chanenel_data(ts_obj, ts_obj_source)
	
	n_channel = ts_obj.GetChannelCount();

	for i = 1:n_channel
		ts_obj.CopyMetaData(ts_obj_source, i, i);
		ts_obj.CopyAttributes(ts_obj_source, i, i);
	end
	
	md_obj = ts_obj.GetMetaData();
	md_obj_source = ts_obj_source.GetMetaData();
	name = md_obj_source.GetItem(0, 'TestName');
	md_obj.SetItem(0, 'InputTestInfo', 'TestName', 'string', name);

	ts_obj.SetXTitle(ts_obj_source.GetXTitle())
	ts_obj.SetXUnits(ts_obj_source.GetXUnits())

end

% 图像显示-单图
function plot_single(x_channel, y_channel, ts_obj, fig_num, plot_type, loc)
	% 单图显示
	[name, xlabel1, ylabel1] = get_data_xy_titles(x_channel, y_channel, ts_obj);
	[xs, ys] = get_data_xy(x_channel, y_channel, ts_obj);
	figure(fig_num);
	subplot(loc);
	hold on ;
	plot(xs, ys, plot_type);
	xlabel(xlabel1);
	ylabel(ylabel1);
	title(name);
end


function [name, xlabel1, ylabel1] = get_data_xy_titles(x_channel, y_channel, ts_obj)
	% 获取横坐标\纵坐标数据\title
	md_obj = ts_obj.GetMetaData();
	name = md_obj.GetItem(0, 'TestName');
	xlabel1 = ts_obj.GetYTitle(x_channel);
	ylabel1 = ts_obj.GetYTitle(y_channel);

	name 	= strrep(name, '_', '-');
	xlabel1 = strrep(xlabel1, '_', '-');
	ylabel1 = strrep(ylabel1, '_', '-');

end

function [xs, ys] = get_data_xy(x_channel, y_channel, ts_obj)
	% 获取指定通道数据作为x,y
	nums = ts_obj.GetPointCount(x_channel);
	xs = ts_obj.GetValues(x_channel, 1, nums);
	ys = ts_obj.GetValues(y_channel, 1, nums);

end
