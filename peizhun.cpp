#include <opencv2/opencv.hpp>
#include "opencv2/core/core.hpp"  
#include "opencv2/highgui/highgui.hpp"  
#include "opencv2/imgproc/imgproc.hpp"  
#include <opencv2/xfeatures2d.hpp>  
#include "opencv2/xfeatures2d/nonfree.hpp"    
//#include "opencv2/legacy/legacy.hpp"   
#include "opencv2/highgui/highgui.hpp"    
#include <math.h>
#include <stdlib.h>
#include <iostream>
#include <algorithm>
using namespace cv;
using namespace std;
using namespace cv::xfeatures2d;
int arry_trans[3] = { 0 };//记录放射变换坐标的位置
Mat M, result, k;
void drawArrow(cv::Mat& img, cv::Point pStart, cv::Point pEnd, int len, int alpha, cv::Scalar& color, int thickness, int lineType)
{
	if (pStart == pEnd)
	{
		//只画一个点
		circle(img, pStart, 1, color);
		return;
	}

	const double PI = 3.1415926;
	Point arrow;
	//计算 θ 角（最简单的一种情况在下面图示中已经展示，关键在于 atan2 函数，详情见下面）   
	double angle = atan2((double)(pStart.y - pEnd.y), (double)(pStart.x - pEnd.x));

	line(img, pStart, pEnd, color, thickness, lineType);

	//计算箭角边的另一端的端点位置（上面的还是下面的要看箭头的指向，也就是pStart和pEnd的位置） 
	arrow.x = pEnd.x + len * cos(angle + PI * alpha / 180);

	arrow.y = pEnd.y + len * sin(angle + PI * alpha / 180);

	line(img, pEnd, arrow, color, thickness, lineType);

	arrow.x = pEnd.x + len * cos(angle - PI * alpha / 180);

	arrow.y = pEnd.y + len * sin(angle - PI * alpha / 180);

	line(img, pEnd, arrow, color, thickness, lineType);
}


//计算质心
float GetCenterOfMass(Mat m)
{
	float m_00 = 0, m_01 = 0, m_10 = 0;

	for (int x = 0; x < m.rows; x++)
	{
		for (int y = 0; y < m.cols; y++)
		{
			m_00 += m.at<uchar>(x, y);
			m_01 += (float)y * m.at<uchar>(x, y);
			m_10 += (float)x * m.at<uchar>(x, y);
		}
	}

	float x_c = m_10 / m_00;
	float y_c = m_01 / m_00;

	return fastAtan2(m_01, m_10);

	//return Point2f(x_c, y_c);
}

//计算灰度直方图
Mat getHistograph(const Mat grayImage)
{
	//定义求直方图的通道数目，从0开始索引  
	int channels[] = { 0 };
	//定义直方图的在每一维上的大小，例如灰度图直方图的横坐标是图像的灰度值，就一维，bin的个数  
	//如果直方图图像横坐标bin个数为x，纵坐标bin个数为y，则channels[]={1,2}其直方图应该为三维的，Z轴是每个bin上统计的数目  
	const int histSize[] = { 256 };
	//每一维bin的变化范围  
	float range[] = { 0,256 };

	//所有bin的变化范围，个数跟channels应该跟channels一致  
	const float* ranges[] = { range };

	//定义直方图，这里求的是直方图数据  
	Mat hist;
	//opencv中计算直方图的函数，hist大小为256*1，每行存储的统计的该行对应的灰度值的个数  
	calcHist(&grayImage, 1, channels, Mat(), hist, 1, histSize, ranges, true, false);

	//找出直方图统计的个数的最大值，用来作为直方图纵坐标的高  
	double maxValue = 0;
	//找矩阵中最大最小值及对应索引的函数  
	minMaxLoc(hist, 0, &maxValue, 0, 0);
	//最大值取整  
	int rows = cvRound(maxValue);
	//定义直方图图像，直方图纵坐标的高作为行数，列数为256(灰度值的个数)  
	//因为是直方图的图像，所以以黑白两色为区分，白色为直方图的图像  
	Mat histImage = Mat::zeros(rows, 256, CV_8UC1);

	//直方图图像表示  
	for (int i = 0; i < 256; i++)
	{
		//取每个bin的数目  
		int temp = (int)(hist.at<float>(i, 0));
		//如果bin数目为0，则说明图像上没有该灰度值，则整列为黑色  
		//如果图像上有该灰度值，则将该列对应个数的像素设为白色  
		if (temp)
		{
			//由于图像坐标是以左上角为原点，所以要进行变换，使直方图图像以左下角为坐标原点  
			histImage.col(i).rowRange(Range(rows - temp, rows)) = 255;
		}
	}
	//由于直方图图像列高可能很高，因此进行图像对列要进行对应的缩减，使直方图图像更直观  
	Mat resizeImage;
	resize(histImage, resizeImage, Size(256, 256));
	return resizeImage;
}

Mat PerspectiveTrans(Mat src, Point2f* scrPoints, Point2f* dstPoints)
{
	Mat dst;
	Mat Trans = getPerspectiveTransform(scrPoints, dstPoints);
	warpPerspective(src, dst, Trans, Size(src.cols, src.rows), CV_INTER_CUBIC);
	return dst;
}
/*************************************************************
*函数名：find_target
*函数功能：寻找对应斜率的点位置
*函数入口：slope,data
*函数返回值：data，数组的位置
**************************************************************/
int find_target(vector <float>slope, float data)
{
	int ans;
	for (int i = 0; i < slope.size(); i++) {
		if (slope[i] == data) {
			return i;
		}
	}
	return -1;
}
/*************************************************************
*函数名：check_point
*函数功能：寻找距离相对较大的匹配点,通过平均值计算
*函数入口：points1,points2,slope,begin（起始位置）,end（结束位置）
*函数返回值：0,1是否满足条件
**************************************************************/
bool check_point(vector <Point2f> points1, vector <Point2f> points2, vector <float>slope, int begin, int end) {
	int count = 0;
	float x_ir_ave = 0, x_vis_ave = 0;
	float temp_pos_value1 = 0, temp_pos_value2 = 0, temp_pos_value3 = 0;//记录下满足条件的坐标，即与平均值较大的坐标但是它不能和其它的点坐标相似
	//计算x坐标的平均值
	for (int i = begin; i <= end; i++) {
		x_ir_ave += points1[find_target(slope, slope[i])].x;
		x_vis_ave += points2[find_target(slope, slope[i])].x;
	}
	x_ir_ave = x_ir_ave / (end - begin + 1);
	x_vis_ave = x_vis_ave / (end - begin + 1);
	//寻找坐标距离差距较大的点
	for (int i = begin; i <= end; i++) {
		if (count == 0) {
			if (abs(points1[find_target(slope, slope[i])].x - x_ir_ave) > 20) {
				temp_pos_value1 = points1[find_target(slope, slope[i])].x;
				arry_trans[0] = find_target(slope, slope[i]);
				count++;
			}
		}
		if (count == 1) {
			if (abs(points1[find_target(slope, slope[i])].x - x_ir_ave) > 20 && abs(points1[find_target(slope, slope[i])].x - temp_pos_value1) > 20) {
				temp_pos_value2 = points1[find_target(slope, slope[i])].x;
				arry_trans[1] = find_target(slope, slope[i]);
				count++;
			}
		}
		if (count == 2) {
			if (abs(points1[find_target(slope, slope[i])].x - x_ir_ave) > 20 && abs(points1[find_target(slope, slope[i])].x - temp_pos_value1) > 20 && abs(points1[find_target(slope, slope[i])].x - temp_pos_value2) > 20) {
				temp_pos_value3 = points1[find_target(slope, slope[i])].x;
				arry_trans[2] = find_target(slope, slope[i]);
				count++;
			}
		}
		if (count >= 3) {
			cout << "红外三个点的坐标是: " << temp_pos_value1 << " " << temp_pos_value2 << " " << temp_pos_value3 << endl;
			return 1;
		}

	}
	return 0;
}
/*************************************************************
*函数名：get_trans_data
*函数功能：获得红外可见光的匹配点后筛选出最好的点用于坐标变换
*函数入口：points1, points2，红外可见光匹配的坐标
*函数返回值：vector <Point2f> 筛选出的最好的匹配点
**************************************************************/
vector <Point2f> get_trans_data(vector <Point2f> points1, vector <Point2f> points2)
{
	vector <Point2f>trans_data;
	vector <float>slope, slope_sort;//定义二维数组存放斜率和对应位置
	//step1 计算红外和可见光对应匹配点的斜率
	for (int i = 0; i < size(points1); i++) {
		slope.push_back((points1[i].y - points2[i].y) / (points1[i].x - points2[i].x));
		slope_sort.push_back((points1[i].y - points2[i].y) / (points1[i].x - points2[i].x));
		cout << "第" << i << "个点的斜率是：" << slope[i] << endl;
	}
	sort(slope_sort.begin(), slope_sort.end());
	//cout << "排序后的斜率是:" << endl;
	//for (vector<float>::iterator it = slope_sort.begin(); it != slope_sort.end(); it++) {
		//cout << *it << " ";
	//}
	int count = 1;
	float temp_data = 0;
	int first_point = 0, last_point = 0;
	//step2 寻找斜率相近的点
	for (int i = 0; i < size(points1) - 1; i++) {
		if (count == 1) {
			if (abs(slope_sort[i] - slope_sort[i + 1]) < 0.2) {
				first_point = i;//记录下当前第一个点的坐标
				temp_data = slope_sort[i];//记录下当前第一个点的斜率
				count++;
			}
		}
		else {
			if (abs(temp_data - slope_sort[i + 1]) < 0.2) { //满足阈值条件自加
				count++;
			}
			else {//至此这个点已经不满足误差条件，将下一个点作为起点继续寻找
				cout << "目前匹配到点数：" << count << endl;
				last_point = i;//记录最后一个点的位置
				if (count >= 3)//放射变换只少要六个参数
				{
					for (int j = first_point; j <= last_point; j++) {
						cout << " " << slope_sort[j] << endl;
						cout << "红外坐标:   " << points1[find_target(slope, slope_sort[j])] << endl;
						cout << "可见光坐标: " << points2[find_target(slope, slope_sort[j])] << endl;
					}
					check_point(points1, points2, slope_sort, first_point, last_point);
				}
				count = 1;//清零，再次寻找
				cout << endl;
			}

		}
	}

	return trans_data;
}
/*************************************************************
*函数名：image_registration
*函数功能：红外可见光配准融合
*函数入口： src1可见光，src2红外
*函数返回值：void
**************************************************************/
void image_registration(Mat src1, Mat src2,int delay)
{
	Mat gray1, gray2;
	cvtColor(src1, gray1, CV_BGR2GRAY);
	cvtColor(src2, gray2, CV_BGR2GRAY);
	double start = static_cast<double>(getTickCount());
	morphologyEx(gray1, gray1, MORPH_GRADIENT, Mat());
	morphologyEx(gray2, gray2, MORPH_GRADIENT, Mat());

	vector<KeyPoint> keypoints_obj, keypoints_sence;
	Mat descriptors_box, descriptors_sence;
	Ptr<ORB> detector = ORB::create();
	Ptr<xfeatures2d::BriefDescriptorExtractor> descriptor = xfeatures2d::BriefDescriptorExtractor::create();
	//Ptr<xfeatures2d::SurfDescriptorExtractor>  descriptor = xfeatures2d::SurfDescriptorExtractor::create();
	detector->detect(gray1, keypoints_sence);
	detector->detect(gray2, keypoints_obj);
	//*******************************************************************************************************************
	/*
	HOGDescriptor descriptor1(Size(16, 16), Size(16, 16), Size(8, 8), Size(8, 8), 9);
	vector<float>hog_points;
	vector<Point>location;
	//KeyPoint::convert(keypoints_obj, location, 1, 1, 0, -1);
	location.push_back(Point(100, 100));
	location.push_back(Point(200, 200));
	descriptor1.compute(gray2, hog_points, Size(0, 0), Size(0, 0), location);
	cout << "descriptor size " << hog_points .size()<<" "<< hog_points[0] <<" " << hog_points[1] << hog_points[2] <<endl;*/
	//********************************************************************************************************************
	descriptor->compute(gray1, keypoints_sence, descriptors_sence);
	descriptor->compute(gray2, keypoints_obj, descriptors_box);
	//detector->detectAndCompute(gray1, Mat(), keypoints_sence, descriptors_sence);
	//detector->detectAndCompute(gray2, Mat(), keypoints_obj, descriptors_box);
	vector<DMatch> matches;
	// 初始化flann匹配BRUTEFORCE_HAMMING

	Ptr<DescriptorMatcher> matcher = makePtr<FlannBasedMatcher>(makePtr<flann::LshIndexParams>(12, 20, 2));
	//Ptr<DescriptorMatcher> matcher = BFMatcher::create(NORM_HAMMING, true);
	matcher->match(descriptors_box, descriptors_sence, matches);
	// 发现匹配

	printf("total match points : %d\n", matches.size());
	//保存匹配对序号  
	vector<int> queryIdxs(matches.size()), trainIdxs(matches.size());
	for (size_t i = 0; i < matches.size(); i++)
	{
		queryIdxs[i] = matches[i].queryIdx;
		trainIdxs[i] = matches[i].trainIdx;
	}
	Mat H12;   //变换矩阵  
	vector<Point2f> points1; KeyPoint::convert(keypoints_obj, points1, queryIdxs);
	vector<Point2f> points2; KeyPoint::convert(keypoints_sence, points2, trainIdxs);
	int ransacReprojThreshold = 5;  //拒绝阈值  
	H12 = findHomography(Mat(points1), Mat(points2), CV_RANSAC, ransacReprojThreshold);
	vector<char> matchesMask(matches.size(), 0);
	Mat points1t;
	perspectiveTransform(Mat(points1), points1t, H12);
	vector<Point2f> points1_match, points2_match;//记录下所有的匹配点
	int mask_sum = 0;
	for (size_t i1 = 0; i1 < points1.size(); i1++)  //保存‘内点’  
	{
		if (norm(points2[i1] - points1t.at<Point2f>((int)i1, 0)) <= ransacReprojThreshold) //给内点做标记  
		{
			matchesMask[i1] = 1;
			points1_match.push_back(points1[i1]);
			points2_match.push_back(points2[i1]);
			mask_sum++;
		}
	}
	Mat Mat_img;
	drawMatches(src2, keypoints_obj, src1, keypoints_sence, matches, Mat_img, Scalar(0, 0, 255), Scalar::all(-1), matchesMask);
	imshow("ransac筛选后", Mat_img);
	double time = ((double)getTickCount() - start) / getTickFrequency();
	cout << "time:" << time << "s" << endl;
	waitKey(delay);
	M = estimateAffine2D(points2_match, points1_match);
	//进行单应性变换
	//cout <<"转换矩阵："<< M << endl;
	//warpPerspective(src2, result, M, src1.size());
	//M = getAffineTransform(vis_match, ir_match);
	if (M.empty()) {
		cout << "转换点不足" << endl;
	}
	else {
		warpAffine(src1, result, M, src2.size());
		imshow("after change", result);
		cout << "after change the ir size is" << result.cols << "*" << result.rows << endl;
		cout << "after change the vis size is" << src2.cols << "*" << src2.rows << endl;
		Mat fusion;
		fusion = result / 2 + src2 / 2;
		imshow("after fusion", fusion);
	}
	
}
int main(int argc, char** argv) {
	//double start = static_cast<double>(getTickCount());
	Mat src, gray1, src2, gray2;
	src = imread("D:\\robot proj\\图像配准融合\\图像配准\\代码\\配准方法集合\\Datasets\\person_vis1.jpg");
	src2 = imread("D:\\robot proj\\图像配准融合\\图像配准\\代码\\配准方法集合\\Datasets\\person_ir1(2).jpg");
	double scale = 0.5;
	Size dsize = Size(src.cols * scale, src.rows * scale);
	Mat src1 = Mat(dsize, CV_32S);
	resize(src, src1, dsize);
	image_registration(src1, src2,1);
	waitKey(0);
	/*
	int count = 0;
	VideoCapture capture_ir("D:\\robot proj\\图像配准融合\\图像配准\\vid1.avi");
	VideoCapture capture_vis("D:\\robot proj\\图像配准融合\\图像配准\\vid11.avi");

	if (!capture_ir.isOpened() && !capture_vis.isOpened())
	{
		cout << "No input imag";
		return 1;
	}
	else
		cout << "yes";
	//获取图像帧率
	long rate = capture_ir.get(CV_CAP_PROP_FRAME_COUNT);
	bool stop = false;
	int delay = 1000 / rate;
	Mat src1, src2;
	//设置开始帧()
	long framecount = 0;
	
	while (framecount != rate)
	{
		if (!capture_ir.read(src1))
			break;
		if (!capture_vis.read(src2))
			break;
		framecount++;
		count++;
		if (count % 2) {
			image_registration(src1, src2, delay);
		}
		else {
			if (M.empty()) {
				cout << "转换点不足" << endl;
			}
			else {
				warpAffine(src2, result, M, src1.size());
				imshow("after change", result);
				cout << "after change the ir size is" << result.cols << "*" << result.rows << endl;
				cout << "after change the vis size is" << src1.cols << "*" << src1.rows << endl;
				Mat fusion;
				fusion = result / 2 + src1 / 2;
				imshow("after fusion", fusion);
			}
		}
	}*/
	return 0;
}